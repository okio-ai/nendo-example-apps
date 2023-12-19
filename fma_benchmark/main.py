import argparse
import os
import random
from typing import List, Dict

from nendo import Nendo, NendoConfig, NendoTrack
from tqdm import tqdm

# suppress TF warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

PROMPT_TEMPLATE = """Please use the following key and values of a description of an audio file to generate a summary of its contents. 
Make sure to keep the summary brief, but include all the information 
especially things like tempo, key, scale and other audio features:"
"""

QUERY_PROMPT_TEMPLATE = """Please use the following key and values of a description of 
an audio file to generate a query to search for similar audio files. Here is an example query:

I want a happy song with a fast tempo and a major key.

Use the following keys and values to generate a query:
REPLY ONLY WITH THE QUERY AND NOTHING ELSE!
"""


def build_simple_query(track: NendoTrack) -> str:
    """Build a simple query from the plugin data of a track."""
    query = "a song"
    moods = track.get_plugin_value("moods")
    if moods is not None:
        mood = random.choice(moods.split(","))
        query = f"a {mood} song"

    key = track.get_plugin_value("key")
    if key is not None:
        query += f" in {key}"

    instruments = track.get_plugin_value("instruments")
    if instruments is not None:
        instrument = random.choice(instruments.split(","))
        query += f" with a {instrument} in it"
    return query

def get_text_from_plugin_data(track: NendoTrack) -> str:
    text = ""
    for key, value in track.meta.items():
        text += f"{key}: {value}; "
    return text


def is_relevant(
        original: NendoTrack, retrieved: List[NendoTrack],
        at: List[int] = (1, 5, 20), threshold: int = 2
) -> Dict[int, int]:
    """Check if the original track is relevant at the given cutoff.

    Works by checking if the original track's plugin data is in the retrieved tracks.

    Args:
        original (NendoTrack): The original track.
        retrieved (List[NendoTrack]): The retrieved tracks.
        at (int, optional): The cutoff. Defaults to 1.
        threshold (int, optional): The number of matches needed to be considered relevant. Defaults to 2.

    Returns:
        bool: True if the original track is relevant, False otherwise.
    """
    scores = {k: 0 for k in at}

    for k in at:
        matches = []
        for t in retrieved[:k]:
            for pd in t.get_plugin_data("nendo_plugin_classify_core"):
                val = pd.value
                if val is not None:
                    for pd in original.get_plugin_data("nendo_plugin_classify_core"):
                        original_val = pd.value
                        if val == original_val or val in original_val:
                            matches.append(val)

            if len(matches) >= threshold:
                scores[k] += 1
    return scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fma_path",
        default="/home/aaron/dev/okio/data/benchmarks/fma_small",
        help="path to the fma dataset",
    )
    parser.add_argument("--mode", default="embed", help="Which mode to run the program in. Either embed or eval.",
                        choices=["embed", "eval"])
    parser.add_argument("--reset", action="store_true", default=False, help="Reset the nendo library.")
    parser.add_argument("--subset", type=int, default=100, help="Number of audio files to evaluate the search on.")
    parser.add_argument(
        "--relevancy_threshold",
        type=int, default=4,
        help="Number of plugin data matches between the original and the query result needed to be considered relevant."
    )
    args = parser.parse_args()

    plugins = [
        "nendo_plugin_embed_clap",
        "nendo_plugin_textgen",
    ]

    if args.mode == "embed":
        plugins.extend([
            "nendo_plugin_caption_lpmusiccaps",
            "nendo_plugin_classify_core",
        ])

    nd = Nendo(
        config=NendoConfig(
            copy_to_library=False,
            auto_convert=False,
            library_path="nendo_library",
            library_plugin="nendo_plugin_library_postgres",
            plugins=plugins
        )
    )

    if args.reset:
        nd.library.reset(force=True)

    if len(nd.library) < 1:
        print("Loading FMA small into nendo library...")
        fma_small = nd.library.add_tracks(path=args.fma_path)
        print(f"Loaded {len(fma_small)} tracks into nendo library.")
    else:
        # we assume we only have one collection in the library with the fma_small data
        colls = nd.library.get_collections()
        print(f"Found {len(colls)} collections in the library.")
        fma_small = nd.library.get_collections()[0]
        # print(f"Found {len(fma_small)} tracks in the collection.")

    errors = []
    if args.mode == "embed":
        print("Running in mode: embed")
        for track in tqdm(fma_small):
            try:
                if len(nd.library.get_embeddings(track_id=track.id)) > 0:
                    print(f"Skipping track {track.id} because it already has an embedding.")
                    continue

                track = nd.plugins.classify_core(track=track)
                track = nd.plugins.caption_lpmusiccaps(track=track)

                summary = nd.plugins.textgen(prompt=PROMPT_TEMPLATE + get_text_from_plugin_data(track))
                track.add_plugin_data("summary", summary, "nendo_plugin_textgen")
                nd.library.embed_track(track=track)
            except Exception as e:
                print(f"Error with track {track.id}: {e}")
                errors.append({
                    "track_id": track.id,
                    "path": track.resource.src,
                    "error": str(e)
                })

        print(f"Finished embedding {len(fma_small)} tracks.")
        print(f"Errors: {len(errors)}")
        print(errors)


    elif args.mode == "eval":
        print("Running in mode: eval")
        if args.subset == -1:
            eval_set = fma_small.tracks()
        else:
            eval_set = fma_small.tracks()
            random.shuffle(eval_set)
            eval_set = eval_set[:args.subset]

        relevant_at_1 = 0
        relevant_at_5 = 0
        relevant_at_20 = 0

        # queries = []
        # queries = nd.plugins.textgen(
        #     prompts=[QUERY_PROMPT_TEMPLATE + get_text_from_plugin_data(t) for t in eval_set],
        #     use_chat=False
        # )

        for track in tqdm(eval_set):
            query = build_simple_query(track)
            tracks = nd.library.nearest_by_query(query, n=20)

            scores = is_relevant(track, tracks, at=[1, 5, 20], threshold=5)
            relevant_at_1 += scores[1]
            relevant_at_5 += scores[5]
            relevant_at_20 += scores[20]

        # TODO reactivate
        # total_relevant = 10  # TODO calculate this, currently an assumption
        # recall_at_1 = relevant_at_1 / total_relevant
        # recall_at_5 = relevant_at_5 / total_relevant
        # recall_at_20 = relevant_at_20 / total_relevant
        #
        # print("Recall @1:", recall_at_1)
        # print("Recall @5:", recall_at_5)
        # print("Recall @20:", recall_at_20)
        #
        # def f1_score(precision, recall):
        #     if precision + recall == 0:
        #         return 0
        #     return 2 * (precision * recall) / (precision + recall)
        #
        # # Calculating F1 score
        # f1_at_1 = f1_score(precision_at_1, recall_at_1)
        # f1_at_5 = f1_score(precision_at_5, recall_at_5)
        # f1_at_20 = f1_score(precision_at_20, recall_at_20)
        #
        # print("F1 @1:", f1_at_1)
        # print("F1 @5:", f1_at_5)
        # print("F1 @20:", f1_at_20)

        precision_at_1 = relevant_at_1 / len(eval_set)
        precision_at_5 = relevant_at_5 / (5 * len(eval_set))
        precision_at_20 = relevant_at_20 / (20 * len(eval_set))

        print("Precision @1:", precision_at_1)
        print("Precision @5:", precision_at_5)
        print("Precision @20:", precision_at_20)


if __name__ == "__main__":
    main()
