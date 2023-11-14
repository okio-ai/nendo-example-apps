# Nendo Video Remixer

The video remixer is an App based on a chain of different nendo plugins. 
It allows you to generate music videos remixed with AI audio from youtube links.

Try it in colab:
<a target="_blank" href="https://colab.research.google.com/github/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/official/model_monitoring/model_monitoring.ipynb">
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

Check out an example:

https://github.com/okio-ai/nendo-example-apps/assets/17432850/c8b445f1-66e9-4d59-add2-3edbfecff457


## Features

- generate music videos of remixed audio from youtube links
- Smells Like Teen Spirit (Dub Version)? Shake It Off (Trash Metal Remix)? Yes please!
- endless creativity, inspiration and memes
- **NEW:** Now comes with stereo generation support from `facebook/musicgen-stereo-*`!

## Installation

Install nendo and the required plugins via `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py -l https://www.youtube.com/watch\?v\=OPf0YbXqDm0 -p "jazz bebop" -o "uptown_jazz.mp4"
```

## Nendo Functionality

### Plugins in use:

- [nendo-plugin-classify-core](https://github.com/okio-ai/nendo_plugin_classify_core)
- [nendo-plugin-stemify-demucs](https://github.com/okio-ai/nendo_plugin_stemify_demucs)
- [nendo-plugin-musicgen](https://github.com/okio-ai/nendo_plugin_musicgen)
- [nendo-plugin-fx-core](https://github.com/okio-ai/nendo_plugin_fx_core)
- nendo-plugin-import-youtube (Coming soon)


The full audio remixing code in this example takes up about 30 lines of code, 
to do MIR, stemification, audio generation and effects processing.
Here is the full example from [main.py](main.py):

```python
def run_nendo_plugin_chain(path_to_audio: str, prompt: str) -> str:
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
    bpm = int(
        float(track.get_plugin_data("nendo_plugin_classify_core", "tempo")[0].value)
    )
    key = track.get_plugin_data("nendo_plugin_classify_core", "key")[0].value
    scale = track.get_plugin_data("nendo_plugin_classify_core", "scale")[0].value

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
        n_samples=1,
        model="facebook/musicgen-stereo-medium",
    )[0]

    vocals = nd.plugins.fx_core.highpass(track=vocals, cutoff_frequency_hz=100)
    vocals = nd.plugins.fx_core.reverb(track=vocals, wet_level=0.2, dry_level=0.8)
    remix = remixed_bg.overlay(vocals, gain_db=1)
    return remix.resource.src
```
