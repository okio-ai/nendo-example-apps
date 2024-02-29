# Polymath

Polymath uses machine learning to convert any music library (*e.g from Hard-Drive or YouTube*) into a music production sample-library. The tool automatically separates tracks into stems (_drums, bass, etc._), quantizes them to the same tempo and beat-grid (*e.g. 120bpm*), analyzes tempo, key (_e.g C4, E3, etc._) and other infos (*timbre, loudness, etc.*) and cuts loop out of them. The result is a searchable sample library that streamlines the workflow for music producers, DJs, and ML audio developers.

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

Please refer to the [polymath requirements](https://github.com/samim23/polymath#requirements) to learn about polymath's requirements.

## Installation

Please refer to the [polymath installation instructions](https://github.com/samim23/polymath#installation) to learn about polymath's requirements.

## Usage

Please refer to the [polymath usage instructions](https://github.com/samim23/polymath#run-polymath) to learn how to use polymath.

## Nendo Functionality

### Plugins in use:

- [nendo-plugin-classify-core](https://github.com/okio-ai/nendo_plugin_classify_core)
- [nendo-plugin-stemify-demucs](https://github.com/okio-ai/nendo_plugin_stemify_demucs)
- [nendo-plugin-quantize-core](https://github.com/okio-ai/nendo_plugin_quantize_core)
- [nendo-plugin-loopify](https://github.com/okio-ai/nendo_plugin_loopify)
