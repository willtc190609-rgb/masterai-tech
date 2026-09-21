import os
import re
import subprocess
import json

POSTS_FILE = os.path.join(os.path.dirname(__file__), 'posts-data.js')

def main():
    print("=" * 60)
    print("  MASTERAI TECH — INSTAGRAM POST AUTO-PUBLISHER")
    print("=" * 60)
    print()

    # Read current posts
    with open(POSTS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine next post number
    matches = re.findall(r'number:\s*"POST #(\d+)"', content)
    if matches:
        next_num = max(int(m) for m in matches) + 1
    else:
        next_num = 9

    post_number_str = f"POST #{next_num:03d}"
    post_id_str = f"post-{next_num:03d}"

    print(f"--> Publishing {post_number_str}")
    print()

    title = input("1. Enter Post Title: ").strip()
    if not title:
        print("Title cannot be empty. Aborted.")
        return

    desc = input("2. Enter Short Description: ").strip()
    if not desc:
        desc = "Latest visual intelligence and technical breakdown from MasterAi Tech."

    print("\nSelect Category:")
    print("  1. AI Tools (tools)")
    print("  2. Model Duel / Comparison (comparison)")
    print("  3. Hardware / PC (hardware)")
    print("  4. AI Fundamentals / Security (fundamentals)")
    cat_choice = input("Enter choice (1-4) [default: 1]: ").strip()
    
    category_map = {
        "1": ("tools", "AI TOOLS", "#38bdf8"),
        "2": ("comparison", "MODEL DUEL", "#ef4444"),
        "3": ("hardware", "HARDWARE", "#f59e0b"),
        "4": ("fundamentals", "AI SECURITY", "#ef4444")
    }
    cat, cat_name, accent = category_map.get(cat_choice, ("tools", "AI TOOLS", "#38bdf8"))

    ig_link = input("\n3. Enter Instagram Post URL (e.g. https://www.instagram.com/p/xxx/): ").strip()
    if not ig_link:
        ig_link = "https://www.instagram.com/MasterAi.CODE/"

    image_url = input("\n4. Enter Cover Image Path or URL [default: assets/covers/cover-post-008.png]: ").strip()
    if not image_url:
        image_url = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=900&q=85"

    tags_input = input("\n5. Enter Tags (separated by comma, e.g. AI, Coding, Hardware): ").strip()
    if tags_input:
        tags = [t.strip() for t in tags_input.split(',') if t.strip()]
    else:
        tags = ["MasterAi", "Tech", "AI"]

    slides_count = input("\n6. Number of slides [default: 5]: ").strip()
    slides_count = int(slides_count) if slides_count.isdigit() else 5

    new_post_obj = {
        "id": post_id_str,
        "number": post_number_str,
        "category": cat,
        "categoryName": cat_name,
        "title": title,
        "description": desc,
        "image": image_url,
        "date": "Sep 2026",
        "slidesCount": slides_count,
        "igLink": ig_link,
        "tags": tags,
        "accentColor": accent
    }

    # Format JSON block with indent
    post_json_block = json.dumps(new_post_obj, indent=4)
    # Adjust indentation to match JS array
    indented_block = "  " + post_json_block.replace("\n", "\n  ") + ",\n"

    # Insert after `const MASTERAI_POSTS = [`
    target_needle = "const MASTERAI_POSTS = ["
    if target_needle in content:
        new_content = content.replace(target_needle, target_needle + "\n" + indented_block, 1)
        with open(POSTS_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\n[✓] Successfully added {post_number_str} to posts-data.js!")
    else:
        print("[!] Error: Could not find MASTERAI_POSTS array in posts-data.js")
        return

    # Git Commit & Push
    print("\n--> Syncing to GitHub 24/7 Live Server...")
    try:
        subprocess.run(["git", "add", "."], check=True, cwd=os.path.dirname(__file__))
        subprocess.run(["git", "commit", "-m", f"Publish {post_number_str}: {title}"], check=True, cwd=os.path.dirname(__file__))
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=os.path.dirname(__file__))
        print("\n" + "=" * 60)
        print(f"  [SUCCESS] {post_number_str} IS NOW LIVE ONLINE 24/7!")
        print("=" * 60)
    except Exception as e:
        print(f"[!] Git sync error: {e}")
        print("You can run 'git push origin main' manually to deploy.")

if __name__ == '__main__':
    main()
