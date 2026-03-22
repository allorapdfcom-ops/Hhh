from flask import Flask, request, jsonify
from flask_cors import CORS   # ✅ ADD THIS
import instaloader

app = Flask(__name__)
CORS(app)   # ✅ ADD THIS

@app.route('/')
def home():
    return "Instagram Downloader API Running 🚀"

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.json
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        loader = instaloader.Instaloader()

        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        response = {
            "caption": post.caption,
            "likes": post.likes,
            "views": post.video_view_count if post.is_video else 0,
            "media": []
        }

        # ✅ VIDEO
        if post.is_video:
            response["media"].append({
                "type": "video",
                "url": post.video_url
            })

        # ✅ IMAGE / CAROUSEL FIX
        elif post.typename == "GraphSidecar":
            for node in post.get_sidecar_nodes():
                if node.is_video:
                    response["media"].append({
                        "type": "video",
                        "url": node.video_url
                    })
                else:
                    response["media"].append({
                        "type": "image",
                        "url": node.display_url
                    })
        else:
            response["media"].append({
                "type": "image",
                "url": post.url
            })

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()            for node in post.get_sidecar_nodes():
                if node.is_video:
                    response["media"].append({
                        "type": "video",
                        "url": node.video_url
                    })
                else:
                    response["media"].append({
                        "type": "image",
                        "url": node.display_url
                    })

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
