import os
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from PIL import Image, ImageTk
import shutil
import platform
import os
import sys
class MinecraftLauncher(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Minecraft Launcher")
        self.geometry("400x300")

        # Load Minecraft logo image and resize it to be 5 times smaller
        original_image = Image.open("minpy.png")  # Replace with the path to your image
        resized_image = original_image.resize((int(original_image.width / 5), int(original_image.height / 5)))
        photo = ImageTk.PhotoImage(resized_image)
        # Display the resized logo
        logo_label = tk.Label(self, image=photo)
        logo_label.image = photo
        logo_label.pack(pady=10)
        self.logo_label = logo_label

        # Create buttons
        singleplayer_button = ttk.Button(self, text="Singleplayer", command=self.show_world_list)
        multiplayer_button = ttk.Button(self, text="Multiplayer", command=self.start_multiplayer)
        quit_button = ttk.Button(self, text="Quit", command=exit)

        # Pack buttons
        singleplayer_button.pack(pady=10)
        multiplayer_button.pack(pady=10)
        quit_button.pack(pady=10)
        self.singleplayer_button = singleplayer_button
        self.multiplayer_button = multiplayer_button
        self.quit_button = quit_button
    def create_world(self):
        # Add code to create a new world file
        new_world_name = filedialog.asksaveasfilename(defaultextension=".json", initialdir=os.path.realpath("./_data/saves/"), filetypes=[("JSON Files", "*.json")])
        if new_world_name:
            with open(new_world_name, "w") as new_world_file:
                # You can initialize the new world file with default settings if needed
                new_world_file.write('{"lib": { "blocks": {}, "entitys": {} },"nlib": { "blocks": {}, "entitys": {} },"elib": { "blocks": {}, "entitys": {} },"glib": { "lib": "lib" }}')
        for button in self.buttons:
            button.destroy()
        self.show_world_list()

    def show_world_list(self):
        self.singleplayer_button.destroy()
        self.multiplayer_button.destroy()
        self.quit_button.destroy()
        self.logo_label.destroy()
        world_frame = ttk.Frame(self)
        world_frame.pack(pady=10)

        # List available worlds
        world_folder = "./_data/saves/"
        worlds = [f for f in os.listdir(world_folder) if f.endswith(".json")]
        self.buttons = []
        self.create_btn = ttk.Button(world_frame, text="Create World", command=self.create_world)
        self.create_btn.pack(pady=5)
        self.buttons.append(self.create_btn)
        # Create buttons for each world
        for world_file in worlds:
            world_name = world_file[:-5]  # Remove the ".txt" extension
            world_button = ttk.Button(world_frame, text=world_name, command=lambda w=world_name: self.show_world_options(w))
            world_button.pack(pady=5)
            self.buttons.append(world_button)
    def show_world_options(self, world_name):
        options_frame = ttk.Frame(self)
        options_frame.pack(pady=10)

        delete_button = ttk.Button(options_frame, text="Delete", command=lambda: self.delete_world(world_name))
        copy_button = ttk.Button(options_frame, text="Copy", command=lambda: self.copy_world(world_name))
        play_button = ttk.Button(options_frame, text="Play", command=lambda: self.play_world(world_name))

        delete_button.pack(side=tk.LEFT, padx=5)
        copy_button.pack(side=tk.LEFT, padx=5)
        play_button.pack(side=tk.LEFT, padx=5)
        self.buttons.append(delete_button)
        self.buttons.append(play_button)
        self.buttons.append(copy_button)
    def delete_world(self, world_name):
        # Add code to delete the selected world file
        world_file_path = f"./_data/saves/{world_name}.json"
        os.remove(world_file_path)
        print(f"Deleting world: {world_name}")
        for button in self.buttons:
            button.destroy()
        self.show_world_list()
    def copy_world(self, world_name):
        # Add code to copy the selected world file
        source = f"./_data/saves/{world_name}.json"
        target = f"./_data/saves/{world_name} copied.json"
        shutil.copyfile(source, target)
        print(f"Copying world: {world_name}")
        for button in self.buttons:
            button.destroy()
        self.show_world_list()
    def play_world(self, world_name):
        # Add code to play the selected world file
        print(f"Playing world: {world_name}")
        try:
            platform.linux_distribution()
            os.system("python"+str(sys.version_info.major)+"."+str(sys.version_info.minor)+" .internal/binariesSource/main.py \""+os.path.realpath(f"./_data/saves/{world_name}.json")+"\" &")
            exit()
        except: 
            if platform.system() == "Windows":
                os.system("start python"+str(sys.version_info.major)+"."+str(sys.version_info.minor)+" .internal/binariesSource/main.py \""+os.path.realpath(f"./_data/saves/{world_name}.json")+"\"")
                exit()
            elif platform.system() == "Darwin":
                os.system("open python"+str(sys.version_info.major)+"."+str(sys.version_info.minor)+" .internal/binariesSource/main.py \""+os.path.realpath(f"./_data/saves/{world_name}.json")+"\"")
                exit()

    def start_multiplayer(self):
        server_ip = simpledialog.askstring("Enter IP", "Enter IP of the server", initialvalue="localhost")
        print("Playing Online Server")
        try:
            platform.linux_distribution()
            os.system("python"+str(sys.version_info.major)+"."+str(sys.version_info.minor)+" .internal/client/main.py \""+server_ip+"\" &")
            exit()
        except: 
            if platform.system() == "Windows":
                os.system("start python"+str(sys.version_info.major)+"."+str(sys.version_info.minor)+" .internal/client/main.py \""+server_ip+"\"")
                exit()
            elif platform.system() == "Darwin":
                os.system("start python"+str(sys.version_info.major)+"."+str(sys.version_info.minor)+" .internal/client/main.py \""+server_ip+"\" &")
                exit()

if __name__ == "__main__":
    app = MinecraftLauncher()
    app.mainloop()
