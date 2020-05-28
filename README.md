### Setup enviroment

#### Package Python

We need some libraries:

- [selenium](https://github.com/SeleniumHQ/selenium): A browser automation framework and ecosystem.
- [pandas](https://github.com/pandas-dev/pandas): Data analysis / manipulation library for Python, providing labeled data structures, statistical functions.
- [youtube_dl](https://github.com/ytdl-org/youtube-dl): Command-line program to download videos from [YouTube](https://www.youtube.com/) and other video sites. Alternative `youtube_dl` is [you-get](https://github.com/soimort/you-get).

```
pip3 install pandas selenium youtube_dl schedule argparse pyvirtualdisplay
```

**Note**: We recommend using [pip](https://pip.pypa.io/en/stable/installing/), but if you are familiar with [Anaconda](https://www.anaconda.com/distribution/), that's okay.

#### Chrome WebDriver

First, download the Chrome WebDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

Then, go to the downloads directory, unzip the file, and move it to `usr/local/bin` PATH.

```
cd Downloads
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
```

**Note**: We recommend using [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads), but if you are familiar with another web drive like [Firefox](https://github.com/mozilla/geckodriver/releases), that's okay.

**Important**: Select the compatible driver for your Chrome version.
