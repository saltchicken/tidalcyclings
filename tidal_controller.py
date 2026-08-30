import subprocess
import threading
import time
import sys
from pathlib import Path

class TidalController:
    def __init__(self, boot_file="BootTidal.hs"):
        print("Starting GHCi and booting TidalCycles...")
        # Spawn the GHCi process
        self.ghci = subprocess.Popen(
            ['ghci'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Consume stdout in a background thread so the pipe buffer doesn't fill and freeze
        threading.Thread(target=self._consume_output, daemon=True).start()

        # Load the BootTidal.hs initialization script
        self.send_command(f":script {boot_file}")
        
        # Give Tidal a moment to boot before accepting new commands
        time.sleep(3)
        print("TidalCycles is ready.")

    def _consume_output(self):
        for line in self.ghci.stdout:
            # You can uncomment the next line to debug GHCi output
            # print(f"[GHCi] {line.strip()}")
            pass

    def send_command(self, cmd):
        # If the command has multiple lines, GHCi requires it to be wrapped in :{ :}
        if '\n' in cmd and not cmd.startswith(':script'):
            payload = ":{\n" + cmd + "\n:}\n"
        else:
            payload = cmd + "\n"
            
        self.ghci.stdin.write(payload)
        self.ghci.stdin.flush()

    def play_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                print(f"Transitioning to: {filepath}")
                self.send_command(f.read())
        except FileNotFoundError:
            print(f"Error: Could not find {filepath}")

if __name__ == "__main__":
    # Initialize the controller
    tidal = TidalController()
    
    while True:
        print("\n--- Tidal Set Controller ---")
        
        # Dynamically find all .tidal files in the current directory
        # Sort them alphabetically for a consistent menu
        tidal_files = sorted(Path('.').glob('*.tidal'))
        
        if not tidal_files:
            print("No .tidal files found in the current directory.")
        else:
            for idx, file_path in enumerate(tidal_files, 1):
                # Format the filename for a cleaner display menu
                display_name = file_path.stem.replace('_', ' ').title()
                print(f"Press {idx}: {display_name}")
                
        print("Type 'q' to quit")
        
        choice = input("\nSelect a track to transition into: ")
        
        if choice.lower() == 'q':
            print("Exiting...")
            sys.exit(0)
            
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(tidal_files):
                selected_file = str(tidal_files[index])
                tidal.play_file(selected_file)
            else:
                print("Invalid choice: Number out of range.")
        else:
            print("Invalid input: Please enter a number or 'q'.")
