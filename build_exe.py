import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "auto_review.py",
        "--onefile",
        "--noconsole",
    ]
)
