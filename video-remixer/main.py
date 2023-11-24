import yt_dlp
import argparse
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip
import os
from nendo import NendoConfig, Nendo


def yt_download(
    link: str,
    output_path: str,
    start_time: str,
    end_time: str,
) -> str:
    start_time = f"00:{start_time}.00"
    end_time = f"00:{end_time}.00"
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": output_path,
        "nocheckcertificate": True,
        "ignoreerrors": True,
        "no_warnings": True,
        "quiet": True,
        "postprocessor_args": [
            "-ss",
            start_time,
            "-to",
            end_time,
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    return f"{output_path}.webm"


def remix_video(video_path: str, audio_path: str, output_path: str) -> str:
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    video_with_audio = video.set_audio(audio)
    video_with_audio.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
    )
    return output_path


def extract_audio(video_path: str, output_path: str) -> str:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,  # Input video file
        "-q:a",
        "0",  # Best audio quality
        "-map",
        "a",  # Map to audio stream
        "-vn",  # No video
        output_path,  # Output audio file
    ]
    subprocess.check_call(cmd)
    return output_path


def run_nendo_plugin_chain(
        path_to_audio: str, prompt: str, vocal_gain: float, model: str,
) -> str:
    nd = Nendo(
        config=NendoConfig(
            plugins=[
                "nendo_plugin_stemify_demucs",
                "nendo_plugin_musicgen",
                "nendo_plugin_classify_core",
                "nendo_plugin_fx_core",
            ],
        )
    )

    track = nd.library.add_track(file_path=path_to_audio)

    track = nd.plugins.classify_core(track=track)
    bpm = int(float(track.get_plugin_data("nendo_plugin_classify_core", "tempo")))
    key = track.get_plugin_data("nendo_plugin_classify_core", "key")
    scale = track.get_plugin_data("nendo_plugin_classify_core", "scale")

    stems = nd.plugins.stemify_demucs(
        track=track, model="mdx_extra", stem_types=["vocals", "no_vocals"]
    )
    vocals, background = stems[0], stems[1]

    remixed_bg = nd.plugins.musicgen(
        track=background,
        prompt=prompt,
        bpm=bpm,
        key=key,
        scale=scale,
        conditioning_length=2,
        n_samples=1,
        model=model,
    )[0]

    vocals = nd.plugins.fx_core.highpass(track=vocals, cutoff_frequency_hz=100)
    vocals = nd.plugins.fx_core.reverb(track=vocals, wet_level=0.2, dry_level=0.8)

    remix = remixed_bg.overlay(vocals, gain_db=vocal_gain)
    return remix.resource.src


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--yt-link",
        type=str,
        required=True,
        help="Youtube link to download for the remix.",
    )
    parser.add_argument(
        "-p", "--prompt", type=str, required=True, help="Prompt to use for the remix."
    )
    parser.add_argument("-s", "--start-time", type=str, default="00:00")
    parser.add_argument("-e", "--end-time", type=str, default="00:30")
    parser.add_argument("-v", "--vocal-gain", type=float, default=0.5)
    parser.add_argument("-m", "--model", type=str, default="facebook/musicgen-stereo-medium")
    parser.add_argument(
        "-o",
        "--output-video-path",
        type=str,
        default="output.mp4",
        help="Output path for the remix.",
    )
    return parser.parse_args()


def main(
    yt_link: str, start_time: str, end_time: str, prompt: str, output_video_path: str, vocal_gain: float, model: str
):
    video_path = yt_download(
        link=yt_link, start_time=start_time, end_time=end_time, output_path="video"
    )
    audio_path = extract_audio(video_path, output_path="audio.mp3")
    remixed_audio_path = run_nendo_plugin_chain(audio_path, prompt, vocal_gain=vocal_gain, model=model)
    remix_video(video_path, remixed_audio_path, output_path=output_video_path)
    os.remove(video_path)
    os.remove(audio_path)


if __name__ == "__main__":
    args = parse_args()
    main(
        yt_link=args.yt_link,
        prompt=args.prompt,
        start_time=args.start_time,
        end_time=args.end_time,
        output_video_path=args.output_video_path,
        vocal_gain=args.vocal_gain,
        model=args.model
    )
