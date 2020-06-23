import glob
import os
import sys
import argparse
from yolo import YOLO, detect_video  # 在文件yolo中导入YOLO类和detect_video函数
from PIL import Image  # 导入文件


def detect_img(yolo):
    while True:
        img = input('Input image filename:')  # 输入图像路径
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(image)  #
            r_image.show()
    yolo.close_session()


def detect_path(yolo):
    dir_path = '/home/huangjx/Projects/kera_ting_yolo3/VOCdevkit/VOC2007/JPEGImages'

    bash_dir = os.path.abspath(dir_path)
    images = []
    images += glob.glob(os.path.join(bash_dir, '*.png'))
    images += glob.glob(os.path.join(bash_dir, '*.jpg'))
    images += glob.glob(os.path.join(bash_dir, '*.jpeg'))

    for num, img_path in enumerate(images):
        dirname, basename = os.path.split(img_path)
        name = basename.split('.', 1)[0]
        path_name = os.path.join(dirname, 'out1')
        if not os.path.exists(path_name):
            os.mkdir(path_name)
        name = name + '_' + str(1) + '.jpg'
        save_name = os.path.join(path_name, name)
        try:
            image = Image.open(img_path)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(image)  #
            # r_image.show()
            r_image.save(save_name)

    yolo.close_session()


FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=True, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str, required=False, default='./path2your_video',
        help="Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help="[Optional] Video output path"
    )

    FLAGS = parser.parse_args()

    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        # detect_img(YOLO(**vars(FLAGS)))
        detect_path(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
