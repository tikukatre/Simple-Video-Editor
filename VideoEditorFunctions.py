from moviepy import *
from moviepy.editor import *
import pandas as pd
from ipywidgets import interact
import ipywidgets as widgets
from IPython.display import Video
import skimage.filters
import logging, sys
logging.disable(sys.maxsize)

formats = {
    'YouTube Shorts, TikTok, Instagram (1080 x 1920)': [1080,1920],
    'Horizontal to Vertical with filled edges (1080 x1920)':[1,1080,1920],
    'YouTube video (1920 x 1080)':[1920,1080],
    'Instagram (1080x1920)': [1080,1920],
    'Twitter Square (720x720)':[720,720],
    'Twitter Landscape (1280x720)':[1280,720],
    'Twitter Portrait (720x1280)':[720,1280],
    'Tiktok (1080x1920)':[1080,1920],
    'Facebook (1280x1920)':[1280,720]
}



def set_file_amount():
    video_amount = widgets.Dropdown(
        options=['1', '2'],
        value='1',
        description='Video amount:',
        disabled=False,
    )
    display(video_amount)

    img_amount = widgets.Dropdown(options=['0', '1'],value='0',description='Image amount:',disabled=False,)
    display(img_amount)

    return video_amount, img_amount





def set_file_locations(video_amount,img_amount):
    video_locations = []
    img_locations = []
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
    imgInputs(int(img_amount.value))
    return video_locations,img_locations


def platform_dropdown():
    platform = widgets.Dropdown(
        options=['YouTube Shorts, TikTok, Instagram (1080 x 1920)','YouTube video (1920 x 1080)',
                 'Horizontal to Vertical with filled edges (1080 x1920)',
                'Twitter Square (720x720)',
                 'Twitter Landscape (1280x720)','Twitter Portrait (720x1280)',
                  'Facebook (1280x1920)'],
        value='YouTube Shorts, TikTok, Instagram (1080 x 1920)',
        description='Platform:',
        disabled=False,
    )
    display(platform)
    return platform

def create_clip(videoFile):
    clip = VideoFileClip(videoFile)
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
    return clip_sub

def create_imgclip(img_path, time, platform):
    img = ImageClip(img_path).set_duration(time)
    img = img.set_duration(time)
    return img

def clip_resize(clip, platform):
    format = formats[platform]
    if (len(format) == 3):
        return horizontal_to_vertical_filled(clip, format)
    w, h = format
    clip_size = clip.size
    if (clip_size[0]>clip_size[1]):
        clip_resized = clip.resize(height=h)
        return clip_resized.crop(x1=1166.6, y1=0, x2=2246.6, y2=1920) #https://stackoverflow.com/questions/69339396/moviepy-how-to-convert-horizontal-video-to-vertical
    else:
        return clip.crop(height=h, y_center=clip.size[1]/2)

def save_video(filename, clip):
    clip.write_videofile(filename+".mp4",remove_temp=True,
                             codec="libx264",
                             audio_codec="aac", fps=30,
                             logger=None, threads=4)
    return clip

def conc_videos(clip1, clip2):
    conc_clips = concatenate_videoclips([clip1,clip2],method='compose')
    return conc_clips

def conc_video_img(clip,imgloc,duration,pos=2):
    #img = ImageClip(imgloc,duration=duration)
    img =ImageSequenceClip([imgloc], fps=duration)
    if(pos==2):
        return concatenate_videoclips([clip,img],method='compose')
    else:
        return concatenate_videoclips([img,clip],method='compose')

def blur(image):
    """ Returns a blurred (radius=2 pixels) version of the image """
    # Increase Sigma for more blurriness
    return skimage.filters.gaussian(image.astype(float), sigma=6)

def horizontal_to_vertical_filled(clip,platform):
    #Horizontal video to vertical with top and bottom filled with blurred version of original
    bg_clip =clip.fl_image(blur)
    bg_clip.add_mask()
    target_width=platform[1]
    target_height=platform[2]
    top_clip=clip.resize(width=target_width)
    bg_clip = bg_clip.resize(height=target_height)
    final = CompositeVideoClip([bg_clip,top_clip.set_position("center")])
    (w,h) = final.size
    return final.crop( width=target_width, height=target_height,x_center=w/2, y_center=h/2)

def vertical_to_horizontal_filled(clip,platform):
    bg_clip = clip.fl_image(blur)
    bg_clip.add_mask()
    target_width = platform[0]
    target_height = platform[1]
    top_clip = clip.resize(height=target_height)
    bg_clip = bg_clip.resize(width=target_width)
    final = CompositeVideoClip([bg_clip, top_clip.set_position("center")])
    (w, h) = final.size
    return final.crop()

def vertical_to_horizontal(clip,sizes):
    black_bg = ImageSequenceClip(["black_img_template.png"],fps=clip.duration).resize(width=sizes[0],height=[1])
    top_clip = clip.resize(sizes[1])
    return  CompositeVideoClip([black_bg, top_clip.set_position("center")])

def save_clip_to_gif(filename,clip,fps=30):
    clip.write_gif(filename+".gif",fps=fps)
    gif = VideoFileClip(filename+".gif")
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

def audio_fade_out(clip,time=0):
    return clip.audio_fadeout(time)

def change_speed(clip,multiplier=0):
    return clip.fx(vfx.speedx, multiplier)

