from tkinter.ttk import Style

settings = {
    "TLabel": {
        
    }
}

marites = Style()
marites.theme_create(
    themename="marites", 
    settings={
        
    }    
)

import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()

    style = ttk.Style()
    
    # Create a new theme based on 'clam'
    style.theme_create('custom_theme', parent='clam', settings={
        'TLabel': {
            'configure': {
                'background': 'lightblue',
                'foreground': 'black',
                'font': ('Helvetica', 12)
            }
        },
        'TButton': {
            'configure': {
                'background': 'blue',
                'foreground': 'white',
                'font': ('Helvetica', 12)
            },
            'map': {
                'background': [('active', 'darkblue')],
                'foreground': [('disabled', 'gray')]
            }
        },
    })

    # Use the custom theme
    style.theme_use('custom_theme')

    # Create and place widgets to see the custom theme in action
    label = ttk.Label(root, text="Custom Themed Label")
    label.pack(pady=10)

    button = ttk.Button(root, text="Custom Themed Button")
    button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
