from moviepy import *
from moviepy.editor import *
from ipywidgets import interact
import ipywidgets as widgets
from IPython.display import Video

formats = {
    'Youtube Shorts (1920x1080)': [1920,1080],
    'Instagram (1080x1920)': [1080,1920],
    'Twitter Square (720x720)':[720,720],
    'Twitter Landscape (1280x720)':[1280,720],
    'Twitter Portrait (720x1280)':[720,1280],
    'Tiktok (1080x1920)':[1080,1920],
    'Facebook (1280x1920)':[1280,720]
}



def set_file_amount():
    def videoDPHandler(wdgt):
        for i in range(int(wdgt.value)):
            print(i)

    video_amount = widgets.Dropdown(
        options=['1', '2'],
        value='1',
        description='Video amount:',
        disabled=False,
    )
    display(video_amount)

    #img_amount = widgets.Dropdown(options=['0', '1'],value='0',description='Image amount:',disabled=False,)
    #display(img_amount)
    return video_amount





def set_file_locations(video_amount):
    video_locations = []
    img_locations = []
    img_amount=0
    def addLocationVideo(wdgt):
        video_locations.append(wdgt.value)

    def videoInputs(amount):
        for i in range(int(amount)):
            fail_loc = widgets.Text(
                value='',
                placeholder='Paste path to the file here.',
                description='Video location:',
                disabled=False
            )
            display(fail_loc)
            fail_loc.on_submit(addLocationVideo)

    def addLocationImg(wdgt):
        img_locations.append(wdgt.value)

    def imgInputs(amount):
        for i in range(int(amount)):
            fail_loc = widgets.Text(
                value='',
                placeholder='Paste path to the file here.',
                description='Img location:',
                disabled=False
            )
            display(fail_loc)
            fail_loc.on_submit(addLocationImg)

    videoInputs(int(video_amount.value))
    imgInputs(int(img_amount))#img_amount.value
    return video_locations,img_locations


def platform_dropdown():
    platform = widgets.Dropdown(
        options=['Youtube Shorts (1920x1080)', 'Twitter Square (720x720)', 'Twitter Landscape (1280x720)',
                 'Twitter Portrait (720x1280)',
                 'Instagram (1080x1920)', 'Facebook (1280x1920)', 'Tiktok (1080x1920)'],
        value='Youtube Shorts (1920x1080)',
        description='Platform:',
        disabled=False,
    )
    display(platform)
    return platform

def display_clip(videoFile):
    clip = VideoFileClip(videoFile)
    #duration = clip.duration
    #clip.ipython_display(width=700, maxduration=duration + 1)
    return clip


def clip_range_slider(clip):
    clip_range = widgets.FloatRangeSlider(
        value=[0, 1],
        min=0,
        max=clip.duration,
        step=0.1,
        description='Clip range:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
    )
    display(clip_range)
    return clip_range

def create_subclip(clip, clip_range):
    clip_sub = clip.subclip(clip_range.value[0], clip_range.value[1])
    #clip_sub.ipython_display(width=700, maxduration=clip_sub.duration + 1)
    return clip_sub

def clip_resize(clip, platform):
    format = formats[platform.value]
    w, h = format
    clip_size = clip.size
    if (clip_size[0]>clip_size[1]):
        clip_resized = clip.resize(height=h)
        return clip_resized.crop(x1=1166.6, y1=0, x2=2246.6, y2=1920)
    else:
        return clip.resize(height=h)

def save_video(filename, clip):
    clip.write_videofile(filename+".mp4")
    return clip

def conc_videos(clip1, clip2):
    conc_clips = concatenate_videoclips([clip1,clip2],method='compose')
    #conc_clips.ipython_display(width=700)
    return conc_clips

def save_clip_to_gif(filename,clip):
    clip.write_gif(filename+".gif")
    # loading  gif
    gif = VideoFileClip(filename+".gif")
    # showing gif
    #gif.ipython_display()
    return gif

def get_text(type):
    text_value=[]
    def replaceText(wdgt):
        if(len(text_value)>0):
            text_value[0] = wdgt.value
        else:
            text_value.append((wdgt.value))


    text = widgets.Text(
        value='',
        placeholder='Write '+type+' here.',
        description='Text:',
        disabled=False
    )
    display(text)
    text.on_submit(replaceText)
    return text_value

def choose_clip():
    file = widgets.Dropdown(
        options=['clip', 'gif'],
        value='clip',
        description='Media to post:',
        disabled=False,
    )
    display(file)
    return file


