# Bubble Sort Visualizer
# Author: Vaibhav Arora - 20473293
# Course: CISC121
# Description: Bubble sort algorithm with the implementation of Gradio

import gradio as gr

# Sorting functions

def parse_input(user_text):
    """Turn '3, 1, 4' into [3, 1, 4]."""
    if not user_text:
        return []

    result = []
    for part in user_text.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            number = int(part)
            result.append(number)
        except ValueError:
            # Skip anything that is not an integer
            continue

    return result


def setup_sorting(input_str):
    """Initialize bubble sort state from the user input."""
    nums = parse_input(input_str)
    length = len(nums)

    state = {
        "arr": nums,
        "i": 0,              # outer loop index (pass)
        "j": 0,              # inner loop index (position in list)
        "n": length,
        "sorted": length <= 1
    }

    if length == 0:
        message = "Enter numbers like: 4, 2, 7, 1"
    else:
        message = "Ready! Press 'Next step' to start bubble sort."

    return str(nums), message, state


def do_one_step(curr_state):
    """Perform one bubble-sort step using the saved state."""
    if curr_state is None or curr_state["n"] == 0:
        return "[]", "You need to click Initialize / Reset first.", curr_state

    arr = curr_state["arr"]
    i = curr_state["i"]
    j = curr_state["j"]
    n = curr_state["n"]

    if curr_state["sorted"]:
        return str(arr), "Already sorted! Final list above.", curr_state

    # End of current pass: move to next pass
    if j >= n - 1 - i:
        i += 1
        j = 0
        if i >= n - 1:
            curr_state["sorted"] = True
            return str(arr), "Sorting finished! List is now sorted.", curr_state
        curr_state["i"] = i
        curr_state["j"] = j
        return str(arr), f"Finished pass {i}. Starting next pass.", curr_state

    # Compare two neighbours
    num1 = arr[j]
    num2 = arr[j + 1]

    if num1 > num2:
        arr[j], arr[j + 1] = arr[j + 1], arr[j]
        explanation = f"Compared {num1} and {num2}: swapped."
    else:
        explanation = f"Compared {num1} and {num2}: kept in place."

    j += 1
    curr_state["arr"] = arr
    curr_state["j"] = j

    return str(arr), explanation, curr_state


# Gradio UI (Blocks + State)

with gr.Blocks() as bubble_app:
    gr.Markdown("# Bubble Sort Visualizer")
    gr.Markdown("Enter numbers, click **Initialize / Reset**, then click **Next step**.")

    # Session state (app memory between clicks)
    memory_state = gr.State()

    input_text = gr.Textbox(
        label="Numbers (comma-separated)",
        placeholder="Try: 3, 5, 2, 8"
    )

    button_reset = gr.Button("Initialize / Reset")
    button_next = gr.Button("Next step")

    list_output = gr.Textbox(label="Current list", interactive=False)
    info_output = gr.Textbox(label="What happened?", interactive=False)

    button_reset.click(
        fn=setup_sorting,
        inputs=[input_text],
        outputs=[list_output, info_output, memory_state],
    )

    button_next.click(
        fn=do_one_step,
        inputs=[memory_state],
        outputs=[list_output, info_output, memory_state],
    )

if __name__ == "__main__":
    bubble_app.launch()
