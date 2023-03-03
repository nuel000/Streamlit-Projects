#importing all dependencies
import streamlit as st
import cv2
from PIL import Image
import numpy as np
from pilgram import css
from pilgram import util
import base64
from io import BytesIO

def dodgeV2(x,y):
    return cv2.divide(x,255-y,scale=256)

#function for download link
def get_image_download(img):
    """
    INPUT : PIL image 
    OUTPUT: html hyperlink 
    """
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/jpg;base64,{img_str}">Download Your Filter Enabled Image </a>'
    return href

#pencil sketch filter

def pencil_sketch(input_image):
    # To convert input image from GBR to Grey
    gray_image = cv2.cvtColor(input_image,cv2.COLOR_BGR2GRAY)
    # Invert our gray image 255-gray image
    invert_image = cv2.bitwise_not(gray_image)
    #Blur the image using guassian function , kernal(21,21)
    blur_image = cv2.GaussianBlur(invert_image,(21,21),sigmaX=0,sigmaY=0)
    #Dodge division
    pencilsketch_image = dodgeV2(gray_image,blur_image)
    return pencilsketch_image

def mayfair(im):
    """Applies Mayfair filter.
    Arguments:
        im: An input image.
    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')
    size = cb.size
    pos = (.4, .4)

    cs1 = util.fill(size, [255, 255, 255, .8])
    cm1 = css.blending.overlay(cb, cs1)

    cs2 = util.fill(size, [255, 200, 200, .6])
    cm2 = css.blending.overlay(cb, cs2)

    cs3 = util.fill(size, [17, 17, 17])
    cm3 = css.blending.overlay(cb, cs3)

    mask1 = util.radial_gradient_mask(size, scale=.3, center=pos)
    cs = Image.composite(cm1, cm2, mask1)

    mask2 = util.radial_gradient_mask(size, length=.3, scale=.6, center=pos)
    cs = Image.composite(cs, cm3, mask2)
    cr = Image.blend(cb, cs, .4)  # opacity

    cr = css.contrast(cr, 1.1)
    cr = css.saturate(cr, 1.1)

    return cr

def brannan(im):
    """Applies Brannan filter.
    Arguments:
        im: An input image.
    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')
    cs = util.fill(cb.size, [161, 44, 199, .31])
    cr = css.blending.lighten(cb, cs)

    cr = css.sepia(cr, .5)
    cr = css.contrast(cr, 1.4)

    return cr

def brooklyn(im):
    """Applies Brooklyn filter.
    Arguments:
        im: An input image.
    Returns:
        The output image.
    """

    cb = util.or_convert(im, "RGB")

    cs1 = util.fill(cb.size, [168, 223, 193, 0.4])
    cm1 = css.blending.overlay(cb, cs1)

    cs2 = util.fill(cb.size, [196, 183, 200])
    cm2 = css.blending.overlay(cb, cs2)

    gradient_mask = util.radial_gradient_mask(cb.size, length=0.7)
    cr = Image.composite(cm1, cm2, gradient_mask)

    cr = css.contrast(cr, 0.9)
    cr = css.brightness(cr, 1.1)

    return cr


def reyes(im):
    """Applies Reyes filter.
    Arguments:
        im: An input image.
    Returns:
        The output image.
    """

    cb = util.or_convert(im, "RGB")

    cs = util.fill(cb.size, [239, 205, 173])
    cs = css.blending.soft_light(cb, cs)
    cr = Image.blend(cb, cs, 0.5)  # opacity

    cr = css.sepia(cr, 0.22)
    cr = css.brightness(cr, 1.1)
    cr = css.contrast(cr, 0.85)
    cr = css.saturate(cr, 0.75)

    return cr

#coding layout and accepting image from user

def main():
    st.title("Instagram Filter App")
    st.markdown("""

                This application applies our regular instagram filters to any photo we choose

                ## `Steps`

                - Upload a picture using the sidebar "Browse files"  button
                - Select the filter you wish to apply from the sidebar
                - Voila!
                """)

    st.write("Select filter to apply")
    file_image = st.sidebar.file_uploader('Upload Image', type=['jpg','jpeg','png'])
    option = st.sidebar.selectbox('Pick a filter',['pencil sketch','brannan','mayfair','brooklyn','reyes'])

    if file_image is None:
        st.write('You have not uploaded any image')
    else:
        if option == "pencil sketch":
            input_image = Image.open(file_image)
            final_sketch = pencil_sketch(np.array(input_image))

            col1, col2 = st.columns(2,gap="large")

            with col1:
                st.markdown("### `Input Image`")
                st.image(input_image, use_column_width=True)


            with col2:
                st.markdown("### `Output Pencil Sketch`")
                st.image(final_sketch, use_column_width=True)
                result = Image.fromarray(final_sketch)
                st.markdown(get_image_download(result), unsafe_allow_html=True)

        elif option == "brannan":
            input_image = Image.open(file_image)
            final_sketch = brannan(input_image)
            col1, col2 = st.columns(2,gap="large")

            with col1:
                st.markdown("### `Input Image`")
                st.image(input_image, use_column_width=True)

            with col2:
                st.markdown("### `Output brannan`")
                st.image(final_sketch, use_column_width=True)
                result = Image.fromarray(np.array(final_sketch))
                st.markdown(get_image_download(result), unsafe_allow_html=True)
                
        elif option == "mayfair":
            input_image = Image.open(file_image)
            final_sketch = mayfair(input_image)

            col1, col2 = st.columns(2,gap="large")

            with col1:
                st.markdown("### `Input Image`")
                st.image(input_image, use_column_width=True)

            with col2:
                st.markdown("### `Output mayfair`")
                st.image(final_sketch, use_column_width=True)
                result = Image.fromarray(np.array(final_sketch))
                st.markdown(get_image_download(result), unsafe_allow_html=True)


        elif option == "brooklyn":
            input_image = Image.open(file_image)
            final_sketch = brooklyn(input_image)

            col1, col2 = st.columns(2,gap="large")

            with col1:
                st.markdown("### `Input Image`")
                st.image(input_image, use_column_width=True)

            with col2:
                st.markdown("### `Output brooklyn`")
                st.image(final_sketch, use_column_width=True)
                result = Image.fromarray(np.array(final_sketch))
                st.markdown(get_image_download(result), unsafe_allow_html=True)


        elif option == "reyes":
            input_image = Image.open(file_image)
            final_sketch = reyes(input_image)

            col1, col2 = st.columns(2,gap="large")

            with col1:
                st.markdown("### `Input Image`")
                st.image(input_image, use_column_width=True)

            with col2:
                st.markdown("### `Output brooklyn`")
                st.image(final_sketch, use_column_width=True)
                result = Image.fromarray(np.array(final_sketch))
                st.markdown(get_image_download(result), unsafe_allow_html=True)


        
if __name__=='__main__':
            main()
