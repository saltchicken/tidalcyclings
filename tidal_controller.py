import subprocess
import threading
import time
import sys
from pathlib import Path

# Embedded priming pattern (using a raw string to preserve Tidal's backslashes)
START_PATTERN = r"""do
  -- Set tempo track to 60 BPM
  p "tempo" $ cps (60/60/4)
  
  let parts = 
        [ ("drums", bd "1*4")
        , ("bass", slow 8 $ note "c3*4" # bass # legato 0.1)
        ]
        
      fx = 
        [ ("fill", fast 2) ]
        
  -- Call the pattern on d1
  d1 $ ur 2 (
    "[drums, bass] \
    \[drums:fill, bass]"
    ) parts fx
"""

class TidalController:
    def __init__(self, boot_file="~/.config/tidal/BootTidal.hs"):
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
                print(f"Playing: {filepath}")
                self.send_command(f.read())
        except FileNotFoundError:
            print(f"Error: Could not find {filepath}")


if __name__ == "__main__":
    # Initialize the controller
    tidal = TidalController()
    
    # Send the embedded pattern immediately after boot
    print("\nPriming system at 60 BPM...")
    tidal.send_command(START_PATTERN)
    
    while True:
        print("\n--- Tidal Set Controller ---")
        
        # Dynamically find all .tidal files in the current directory
        tidal_files = sorted(Path('.').glob('*.tidal'))
        
        if not tidal_files:
            print("No .tidal files found in the current directory.")
        else:
            for idx, file_path in enumerate(tidal_files, 1):
                # Format the filename for a cleaner display menu
                display_name = file_path.stem.replace('_', ' ').title()
                print(f"Press {idx}: {display_name}")
                
        print("\nType 'r' to refresh the list")
        print("Type 'q' to quit")
        
        choice = input("\nSelect an action: ")
        
        if choice.lower() == 'q':
            print("Exiting...")
            sys.exit(0)
            
        if choice.lower() == 'r':
            print("Refreshing file list...")
            continue
            
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(tidal_files):
                selected_file = str(tidal_files[index])
                tidal.play_file(selected_file)
            else:
                print("Invalid choice: Number out of range.")
        else:
            print("Invalid input: Please enter a number, 'r', or 'q'.")
