# Nendo Video Remixer

The video remixer is an App based on a chain of different nendo plugins. 
It allows you to generate music videos remixed with AI audio from youtube links.

**⚠ Important Disclaimer:** 
The video/audio content created using Remix are intended solely for research and educational purposes. 
We assume no responsibility for their use or misuse. 
We urge users to employ this tool responsibly and ethically.

Try it in colab:
<a target="_blank" href="https://colab.research.google.com/drive/1P1BEArCX9kRVVqTbZXxX3eFevxvjuVpq?usp=sharing">
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

Check out an example:

https://github.com/okio-ai/nendo-example-apps/assets/17432850/061a07a2-64ac-4647-872a-8b6f1370fab8


## Features

- Generate music videos of remixed audio from youtube links
- Smells Like Teen Spirit (Dub Version)? Shake It Off (Trash Metal Remix)? Yes please!
- Endless creativity, inspiration and memes

## Requirements

As this app uses the [Nendo musicgen plugin](https://github.com/okio-ai/nendo_plugin_musicgen), you have to install Pytorch 2.0.0 or higher first:

`pip install "torch>=2.0"`

> Note: On Mac OSX, the instructions for installing pytorch differ. Please refer to the [pytorch installation instructions](https://pytorch.org/get-started/locally/).

## Installation

Install nendo and the required plugins via `requirements.txt`:

```bash
git clone https://github.com/okio-ai/nendo-example-apps.git
cd nendo-example-apps/video-remixer
pip install -r requirements.txt
```

## Usage

Create a video remix from a youtube link:

```bash
python main.py -l https://www.youtube.com/watch\?v\=OPf0YbXqDm0 -p "jazz bebop" -o "uptown_jazz.mp4" 
```

Create an audio-only remix from a file:

```bash
python main.py -f /path/to/file.mp3 -p "jazz bebop" -oa "jazz_remix.mp3" 
```

## Nendo Functionality

### Plugins in use:

- [nendo-plugin-classify-core](https://github.com/okio-ai/nendo_plugin_classify_core)
- [nendo-plugin-stemify-demucs](https://github.com/okio-ai/nendo_plugin_stemify_demucs)
- [nendo-plugin-musicgen](https://github.com/okio-ai/nendo_plugin_musicgen)
- [nendo-plugin-fx-core](https://github.com/okio-ai/nendo_plugin_fx_core)


The full audio remixing code in this example takes up about 30 lines of code, 
to do MIR, stemification, audio generation and effects processing.
Here is the full example from [main.py](main.py):

```python
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
```

