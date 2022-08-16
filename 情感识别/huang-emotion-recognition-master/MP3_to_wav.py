from ffmpy import FFmpeg as mpy
import os


def read_folder(mp3_folder, wav_folder):
    for a in os.listdir(mp3_folder):
        # 创建MP3文件的绝对路径
        mp3_file = os.path.join(mp3_folder, a)
        # 调用格式转换函数
        trans_to_wav(mp3_file, wav_folder)

def trans_to_wav(mp3_file, wav_folder):
    # 格式化文件
    file_fmt = os.path.basename(mp3_file).strip()
    # 获取文件格式
    file_fmt = file_fmt.split('.')[-1]
    # 校验文件格式
    if file_fmt.strip() != 'mp3':
        raise Exception('改文件不是MP3格式，请检查！')
    elif file_fmt.strip() == '':
        raise Exception('文件格式出现异常，请检查！')
    # 创建wav的文件以供转换完成后输出
    wav_file_path = os.path.join(wav_folder)
    wav_file_path = os.path.join(wav_file_path, '{}.{}'.format(
        os.path.basename(mp3_file).strip().split('.')[0], 'wav'
    ))
    # 创建转换时的命令行参数字符串
    cmder = '-f wav -ac 1 -ar 16000'
    # 创建转换器对象
    mpy_obj = mpy(
        inputs={
            mp3_file: None
        },
        outputs={
            wav_file_path: cmder
        }
    )
    print('执行CMDER 命令：{}'.format(mpy_obj.cmd))

    # 执行转换
    mpy_obj.run()

if __name__ == '__main__':
    '''
    主函数入口
    '''
    # 输入MP3文件夹
    mp3_folder = input('输入MP3文件夹路径：\n')
    # 校验MP3文件夹是否存在
    if mp3_folder.strip() == '':
        raise Exception('输入空值，请检查！')
    elif mp3_folder.strip() != '':
        if os.path.exists(mp3_folder) is False:
            raise Exception('文件路径不存在')
    # 输入wav文件夹路径
    wav_folder = input('输入wav文件夹路径：\n')
    # 校验wav文件夹是否存在
    if wav_folder.strip() == '':
        raise Exception('输入空值，请检查！')
    elif wav_folder.strip() != '':
        if os.path.exists(wav_folder) is False:
            raise Exception('文件路径不存在')
    # 调用文件夹读取批量文件
    read_folder(mp3_folder, wav_folder)

