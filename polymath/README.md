# Polymath

Polymath uses machine learning to convert any music library (e.g from Hard-Drive or YouTube) into a music production sample-library. The tool automatically separates songs into stems (beats, bass, etc.), quantizes them to the same tempo and beat-grid (e.g. 120bpm), analyzes musical structure (e.g. verse, chorus, etc.), key (e.g C4, E3, etc.) and other infos (timbre, loudness, etc.), and converts audio to midi. The result is a searchable sample library that streamlines the workflow for music producers, DJs, and ML audio developers.

Try it in colab:
<a target="_blank" href="https://colab.research.google.com/drive/1TjRVFdh1BPdQ_5_PL5EsfS278-EUYt90?usp=sharing">
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Features

- Import tracks from youtube or directly from your google drive
- Process selected (or all) tracks with a configurable selection of nendo plugins:
    - Apply the [classification plugin](https://github.com/okio-ai/nendo-plugin-classify-core) to compute _volume_, _tempo_ (bpm), _key_, _intensity_, _frequency_, and _loudness_ for each track
    - Apply the [stemification plugin](https://github.com/okio-ai/nendo-plugin-stemify-demucs) to separate each track into four source signals: _vocals_, _drum_, _bass_, and _other_
    - Apply the [quantization plugin](https://github.com/okio-ai/nendo-plugin-quantize-core) to quantize each track to a specified target _bpm_
    - Apply the [loopification plugin](https://github.com/okio-ai/nendo-plugin-loopify) to automatically detect and extract loops from each sample
- Export the results of the processing with informative file names to your google drive in _wav_, _mp3_ or _ogg_ format.

## Requirements

The [quantizer plugin](https://github.com/okio-ai/nendo-plugin-quantize-core) requires the `rubberband` package to be installed in your system. Please refer to the [rubberband documentation](https://breakfastquay.com/rubberband/index.html) for further information.

Due to errors with `madmom` versions < 0.17 errors and python 3.10, the [loopify plugin](https://github.com/okio-ai/nendo-plugin-loopify) requires the latest version of the  package from git, where this is fixed. See also [this related issue](https://github.com/CPJKU/madmom/issues/502).

Run:

`pip install git+https://github.com/CPJKU/madmom.git@0551aa8`

## Installation

Clone the [polymath](https://github.com/samim23/polymath) repository and install nendo and the required plugins via `requirements.txt`:

```bash
git clone https://github.com/samim23/polymath
cd polymath
pip install -r requirements.txt
```

## Usage

Please refer to the [polymath usage instructions](https://github.com/samim23/polymath#run-polymath) to learn how to use polymath.

## Nendo Functionality

### Plugins in use:

- [nendo-plugin-classify-core](https://github.com/okio-ai/nendo_plugin_classify_core)
- [nendo-plugin-stemify-demucs](https://github.com/okio-ai/nendo_plugin_stemify_demucs)
- [nendo-plugin-quantize-core](https://github.com/okio-ai/nendo_plugin_quantize_core)
- [nendo-plugin-loopify](https://github.com/okio-ai/nendo_plugin_loopify)
