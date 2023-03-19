import tkinter as tk
from tkinter import filedialog, messagebox
import spectral
import matplotlib.pyplot as plt
import matplotlib

# Create the main window
root = tk.Tk()

# Define the function to handle the file button click
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("LAN files", "*.lan")])
    if file_path:
        # Load the LAN image
        img = spectral.open_image(file_path)

        # Get the number of bands in the image
        n_bands = img.shape[2]

        # Determine the number of pages required to display all the bands
        n_pages = n_bands // 4
        if n_bands % 4 != 0:
            n_pages += 1

        # Create a figure to display the images
        fig, axs = plt.subplots(2, 2, figsize=(12, 12))

        # Flatten the list of axes
        axs = axs.flatten()

        # Remove unused axes
        for i in range(n_bands, 4):
            fig.delaxes(axs[i])

        # Add a title to the figure indicating the current page
        suptitle = fig.suptitle("Page 1 of {}".format(n_pages))

        # Display the first 4 bands
        for i in range(4):
            axs[i].imshow(img[:, :, i], cmap="gray")
            axs[i].set_title("Band {}".format(i+1))

        # Create a next button
        next_button = matplotlib.widgets.Button(plt.axes([0.8, 0.05, 0.1, 0.075]), "Next")

        # Define the function to be called when the next button is clicked
        def next_button_clicked(event):
            current_page = int(suptitle.get_text().split()[1])
            if current_page == n_pages:
                return
            current_page += 1
            suptitle.set_text("Page {} of {}".format(current_page, n_pages))
            for i in range(4):
                axs[i].imshow(img[:, :, (current_page-1)*4 + i], cmap="gray")
                axs[i].set_title("Band {}".format((current_page-1)*4 + i + 1))
            fig.canvas.draw_idle()

        # Connect the next button to the function
        next_button.on_clicked(next_button_clicked)

        # Hide the main window
        root.withdraw()

        # Display the figure
        plt.show()

# Define the function to handle the login button click
def login():
    messagebox.showinfo("Login", "You are now logged in to the USGS EarthExplorer database.")

    # Hide the main window
    root.withdraw()

    # Display the plot
    select_file()

# Create the welcome label
welcome_label = tk.Label(root, text="Welcome to HyperGix 1.5!", font=("Arial", 20))
welcome_label.pack(pady=20)

# Create the file button
file_button = tk.Button(root, text="Select File", command=select_file)
file_button.pack(pady=10)

# Create the login button
login_button = tk.Button(root, text="Login to USGS EarthExplorer", command=login)
login_button.pack(pady=10)

# Run the main loop
root.mainloop()
