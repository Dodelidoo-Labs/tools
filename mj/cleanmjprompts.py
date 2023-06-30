import csv
import re
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import threading
import queue

def normalize_numbers_in_string(input_string):
    # Regular expression pattern to find numbers in the string
    number_pattern = r"[-+]?\d*\.?\d+(?:,\d+)?"

    # Find the valid numbers in the input string
    numbers = re.findall(number_pattern, input_string)
    numbers = [float(num.replace(',', '')) for num in numbers if num.strip()]

    # Check if any valid numbers were found
    if not numbers:
        return input_string

    min_value = min(numbers)
    max_value = max(numbers)

    # Check if the range is zero
    if max_value == min_value:
        return input_string

    def normalize(match):
        number = float(match.group().replace(',', ''))
        # Normalize the number between 0 and 1
        normalized_number = (number - min_value) / (max_value - min_value)
        return str(normalized_number)

    # Use re.sub() with a custom function to replace numbers with normalized values
    normalized_string = re.sub(number_pattern, normalize, input_string)

    return normalized_string

def replace_double_colons(input_string):
    # Find all occurrences of double colons and replace them with single colons
    modified_string = input_string.replace("::", ":")
    return modified_string

def remove_after_second_hashtag(text):
    hashtags = text.split("**")
    if len(hashtags) >= 3:
        new_text = '**'.join(hashtags[:2])
        return new_text
    return text

def clean_data(input_file, output_file, progress_queue):

    with open(input_file, 'r', errors='ignore') as file:
        reader = csv.reader(file)
        data = list(reader)

    length_data = len(data)
    for i, row in enumerate(data):
        progress = (i + 1) / length_data * 100
        progress_queue.put(progress)

        prompt = row[0]

        # Remove double asterisks (**) from the first column
        prompt = remove_after_second_hashtag(prompt)
        prompt = prompt.replace('**', '')

        # Remove text after the first double dash (--)
        #double_dash_index = prompt.find('--')
        #if double_dash_index != -1:
            #prompt = prompt[:double_dash_index]
            #prompt = prompt.replace('--', '')

        # Remove text after the Image # occurrence
        #image_string_index = prompt.find('- Image')
        #if image_string_index != -1:
            #prompt = prompt[:image_string_index]
            #prompt = prompt.replace('- Image', '')

        # Remove text after the Image # occurrence
        #upscaled_string_index = prompt.find('- Upscaled')
        #if upscaled_string_index != -1:
            #prompt = prompt[:upscaled_string_index]
            #prompt = prompt.replace('- Upscaled', '')

        # Normalise weights
        #prompt = normalize_numbers_in_string(prompt)

        # Replace double colons
        #prompt = replace_double_colons(prompt)

        # Replace link pointers and Prompt text
        prompt = prompt.replace("Prompt", "")

        # Remove consecutive spaces
        prompt = re.sub(r' +', ' ', prompt)

        # Remove leading and trailing spaces
        prompt = prompt.strip()

        row[0] = prompt

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    progress_queue.put('done')

# GUI
def update_progress(root, progress_var, progress_queue, run_button, complete_label):
    while not progress_queue.empty():
        progress = progress_queue.get()
        if progress == 'done':
            run_button.config(state='normal')
            progress_var.set(0)  # reset progress bar
            complete_label.pack(side='bottom')  # show the label when the process is done
            break
        progress_var.set(progress)
    root.after(100, update_progress, root, progress_var, progress_queue, run_button, complete_label)

def open_file_dialog(entry_field):
    file_path = filedialog.askopenfilename()
    entry_field.delete(0, END)
    entry_field.insert(0, file_path)

def save_file_dialog(entry_field):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv")
    entry_field.delete(0, END)
    entry_field.insert(0, file_path)

def run_process(input_field, output_field, progress_var, root, run_button, complete_label):
    input_file = input_field.get()
    output_file = output_field.get()

    run_button.config(state='disabled')
    complete_label.pack_forget()  # hide the label when the process starts

    progress_queue = queue.Queue()
    threading.Thread(target=clean_data, args=(input_file, output_file, progress_queue)).start()
    root.after(100, update_progress, root, progress_var, progress_queue, run_button, complete_label)

def main():
    root = Tk()
    root.geometry('500x300')

    # Create a label with a complete text, initially hidden
    complete_label = Label(root, text="✔ Process Complete", fg="green")
    complete_label.pack_forget()  # Use pack_forget instead of grid_remove

    Label(root, text='Input File:').pack()
    input_entry = Entry(root, width=50)
    input_entry.pack()
    Button(root, text='Select', command=lambda: open_file_dialog(input_entry)).pack()

    Label(root, text='Output File:').pack()
    output_entry = Entry(root, width=50)
    output_entry.pack()
    Button(root, text='Select', command=lambda: save_file_dialog(output_entry)).pack()

    progress_var = DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.pack(fill=X)

    run_button = Button(root, text='Run', command=lambda: run_process(input_entry, output_entry, progress_var, root, run_button, complete_label))
    run_button.pack(side='top')

    root.mainloop()

if __name__ == '__main__':
    main()
