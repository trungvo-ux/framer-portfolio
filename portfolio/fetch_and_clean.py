import os
import subprocess
import sys
import shutil
from urllib.parse import urlparse

# python3 fetch_and_clean.py {framer url}
# python3 fetch_and_clean.py https://kind-action-155196.framer.app/


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_and_clean.py <target_url>")
        sys.exit(1)

    target_url = sys.argv[1]
    parsed_url = urlparse(target_url)
    domain = parsed_url.netloc
    
    # The wget command requested
    wget_command = [
        "wget",
        "--mirror",
        "--page-requisites",
        "--convert-links",
        "--adjust-extension",
        "--no-parent",
        "-e", "robots=off",
        target_url
    ]

    print(f"Downloading {target_url}...")
    try:
        subprocess.run(wget_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running wget: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'wget' command not found. Please install wget.")
        sys.exit(1)

    # The directory created by wget is usually the domain name
    download_dir = domain
    
    if not os.path.exists(download_dir):
        print(f"Expected download directory '{download_dir}' not found.")
        sys.exit(1)

    print(f"Processing files in {download_dir}...")

    # The string to remove
    badge_code = '<div id="__framer-badge-container"><!--$--><!--$--><!--$--><a class="framer-6jWyo framer-n0ccwk framer-v-n0ccwk framer-bmpgw8 __framer-badge" data-framer-appear-id="n0ccwk" data-framer-name="Light" data-nosnippet="true" style="will-change:transform;pointer-events:auto;opacity:0.001;transform:translateY(10px)" href="https://www.framer.com" rel="noopener" title="Create a free website with Framer, the website builder loved by startups, designers and agencies."><div class="framer-13yxzio" data-framer-name="Backdrop" style="background-color:rgb(255, 255, 255);border-bottom-left-radius:10px;border-bottom-right-radius:10px;border-top-left-radius:10px;border-top-right-radius:10px;box-shadow:0px 0.6021873017743928px 1.5656869846134214px -1.5px rgba(0, 0, 0, 0.17), 0px 2.288533303243457px 5.950186588432988px -3px rgba(0, 0, 0, 0.14), 0px 10px 26px -4.5px rgba(0, 0, 0, 0.02)"></div><div class="framer-19yaanm" data-framer-name="Content" style="transform:translate(-50%, -50%)"><div class="framer-1kflzx5"><div data-framer-name="Logo" class="framer-hcsc7 framer-e50co" style="--1bd4d3i:rgb(0, 0, 0);--otdjsv:rgb(0, 0, 0);transform:translateX(-50%)"></div></div><!--$--><p style="position:absolute;transform:scale(0.001)">Create a free website with Framer, the website builder loved by startups, designers and agencies.</p><div data-framer-name="Text" class="framer-g7oZR framer-1um7t9d" style="--1bd4d3i:rgb(0, 0, 0);--otdjsv:rgb(0, 0, 0)"></div><!--/$--></div><div class="framer-j4ugry" data-framer-name="Bottom" style="mask:linear-gradient(180deg, rgba(0,0,0,0) 65%, rgba(0,0,0,1) 100%) add;-webkit-mask:linear-gradient(180deg, rgba(0,0,0,0) 65%, rgba(0,0,0,1) 100%) add;border-bottom-left-radius:11px;border-bottom-right-radius:11px;border-top-left-radius:11px;border-top-right-radius:11px;box-shadow:inset 0px 0px 0px 1px rgb(0, 0, 0);opacity:0.06"></div><div class="framer-jnuwbw" data-framer-name="Border" style="border-bottom-left-radius:11px;border-bottom-right-radius:11px;border-top-left-radius:11px;border-top-right-radius:11px;box-shadow:inset 0px 0px 0px 1px rgb(0, 0, 0);opacity:0.04"></div></a><!--/$--><!--/$--><!--/$--></div>'

    # Walk through the directory
    for root, dirs, files in os.walk(download_dir):
        for file in files:
            if file.endswith(".html"):
                source_path = os.path.join(root, file)
                
                # Calculate destination path (relative to current dir, preserving structure inside domain folder)
                rel_path = os.path.relpath(source_path, download_dir)
                dest_path = os.path.join(".", rel_path)
                
                # Create directories if needed
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Remove the badge and save to new location
                try:
                    with open(source_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if badge_code in content:
                        print(f"Removing badge from {source_path}")
                        content = content.replace(badge_code, "")
                    
                    with open(dest_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Moved and cleaned: {dest_path}")
                except Exception as e:
                    print(f"Error processing HTML file {source_path}: {e}")
            
    # Remove the original download directory and everything in it
    print(f"Cleaning up {download_dir}...")
    try:
        shutil.rmtree(download_dir)
    except Exception as e:
        print(f"Error removing directory {download_dir}: {e}")

    print("Done.")

if __name__ == "__main__":
    main()
