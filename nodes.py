#  Package Modules
import csv
import os

#  ComfyUI Modules
import folder_paths
from comfy.utils import ProgressBar

#  Basic practice to get paths from ComfyUI
custom_nodes_script_dir = os.path.dirname(os.path.abspath(__file__))
custom_nodes_model_dir = os.path.join(folder_paths.models_dir, "my-custom-nodes")
custom_nodes_output_dir = os.path.join(folder_paths.get_output_directory(), "my-custom-nodes")


#  These are example nodes that only contains basic functionalities with some comments.
#  If you need detailed explanation, please refer to : https://docs.comfy.org/essentials/custom_node_walkthrough
#  First Node:


def read_ratio_presets():
    p = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(p, "preset_ratios.csv")
    preset_ratios_dict = {}
    labels = []
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter="|", quotechar='"')
        for row in reader:
            preset_ratios_dict[row[0]] = [row[1], row[2]]
            labels.append(row[0])
    return preset_ratios_dict, labels


class SimpleRatioSelector:
    @classmethod
    def INPUT_TYPES(s):
        s.ratio_presets = read_ratio_presets()[1]
        s.preset_ratios_dict = read_ratio_presets()[0]
        return {
            "required": {
                "select_preset": (
                    s.ratio_presets,
                    {
                        "default": s.ratio_presets[0],
                        "tooltip": "Select a preset dimensions (Width x Height)",
                    },
                ),
                "portrait": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "This flips the orientation from landscape (Width x Height) to portrait (Height x Width)",
                    },
                ),
            },
            "hidden": {"unique_id": "UNIQUE_ID", "extra_pnginfo": "EXTRA_PNGINFO", "prompt": "PROMPT"},
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    CATEGORY = "utils"
    FUNCTION = "run"

    def run(self, select_preset, portrait, unique_id=None, extra_pnginfo=None, prompt=None):
        width, height = self.preset_ratios_dict[select_preset] # sample output: ['1920', '1080']
        
        #  If portrait is True, flip the width and height
        if portrait:
            width, height = height, width

        return (int(width), int(height))
