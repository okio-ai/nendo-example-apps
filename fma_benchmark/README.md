# Nendo Search FMA Benchmark

This search benchmark showcases the performance of Nendo being used as a Audio Search Engine.
It uses the [fma_small](https://github.com/mdeff/fma) dataset, consisting of 8,000 tracks with a length of 30s.

**Current results:**

| Relevancy Threshold | Precision @1 | Precision @5 | Precision @20  |
|---------------------|--------------|--------------|----------------|
| 5                   | 0.031        | 0.71985      | 0.92945        |
| 4                   | 0.19275      | 0.8018       | 0.950125       |
| **3**               | **0.46875**  | **0.87775**  | **0.96914375** |
| 2                   | 0.78525      | 0.953        | 0.98796875     |
| 1                   | 0.956        | 0.990625     | 0.997375       |

### relevancy_threshold

To evaluate if a track is relevant to a query, we use the `relevancy_threshold` parameter.
This parameter defines how many of a tracks analysis plugin data points have to match the query to be considered
relevant.
For example, if we set `relevancy_threshold = 1` and the query has a `tempo` of `120`,
a track is already considered relevant if it has a `tempo` of `120` as well. Even if all the other tags like `moods`
or `instruments` don't match at all.

If we set `relevancy_threshold = 5` on the other hand, a track is only considered relevant if `>=5` tags match the
query.

### Building queries

We have two ways of building queries:

#### 1. Using the a simple string builder with random tracks tags:

We build queries by randomly sampling from a tracks `moods`, `instruments` and `key` tags.
An example query would then look like this:

```pycon
>>> build_simple_query(track)
"a sad song in A minor with a piano in it"
```

#### 2. Using the `nendo_plugin_textgen` plugin:

We build queries by using the `nendo_plugin_textgen` plugin.
This plugin allows us to generate text from a given prompt using a local LLM.
We use the following prompt to generate queries:

```
Please use the following key and values of a description of 
an audio file to generate a query to search for similar audio files. Here is an example query:

I want a happy song with a fast tempo and a major key.

Use the following keys and values to generate a query:
REPLY ONLY WITH THE QUERY AND NOTHING ELSE!
```

## Requirements

Please make sure that you downloaded the [fma_small](https://github.com/mdeff/fma) dataset before running the benchmark.

To run `nendo_plugin_library_postgres` you need to have a postgres database running, please refer to
the [plugin documentation](https://okio.ai/docs/plugins) for more information how to set this up.

## Installation

Install nendo and the required plugins via `requirements.txt`:

```bash
git clone https://github.com/okio-ai/nendo-example-apps.git
cd nendo-example-apps/fma_benchmark
pip install -r requirements.txt
```

## Usage

Before running the evaluation you have to embed the audio files using our analysis and embedding plugins, please run:

```bash
python main.py --fma_path /path/to/fma_small --mode embed
```

This will probably take a while! After the embedding is done, you can run the evaluation:

```bash
python main.py --mode eval --subset -1 --relevancy_threshold 4
```

Per default this will give you `Precision @1`, `Precision @5` and `Precision @20` for the whole dataset.

## Nendo Functionality

### Plugins in use:

- [nendo-plugin-classify-core](https://github.com/okio-ai/nendo_plugin_classify_core)
- [nendo-plugin-embed-clap](https://github.com/okio-ai/nendo_plugin_embed_clap)
- [nendo-plugin-library-postgres](https://github.com/okio-ai/nendo_plugin_library_postgres)
- [nendo-plugin-textgen](https://github.com/okio-ai/nendo_plugin_textgen)
- [nendo-plugin-caption-lpmusiccaps](https://github.com/okio-ai/nendo_plugin_caption_lpmusiccaps)

## Notes

- `relevancy_threshold = 5`
  Precision @1: 0.031
  Precision @5: 0.71985
  Precision @20: 0.92945
- `relevancy_threshold = 4`
  Precision @1: 0.19275
  Precision @5: 0.8018
  Precision @20: 0.950125

- `relevancy_threshold = 3`
  Precision @1: 0.46875
  Precision @5: 0.87775
  Precision @20: 0.96914375

- `relevancy_threshold = 2`
  Precision @1: 0.78525
  Precision @5: 0.953
  Precision @20: 0.98796875

- `relevancy_threshold = 1`
  Precision @1: 0.956
  Precision @5: 0.990625
  Precision @20: 0.997375
