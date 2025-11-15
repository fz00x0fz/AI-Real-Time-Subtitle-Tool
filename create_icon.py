"""
创建应用图标
如果没有icon.ico文件，运行此脚本生成一个简单的图标
"""
try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_icon():
        """创建应用图标"""
        # 创建256x256的图像
        size = 256
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制圆形背景
        margin = 20
        draw.ellipse(
            [margin, margin, size-margin, size-margin],
            fill=(0, 217, 255, 255),  # 青色
            outline=(255, 255, 255, 255),
            width=8
        )
        
        # 绘制麦克风图标（简化版）
        center_x = size // 2
        center_y = size // 2
        
        # 麦克风主体
        mic_width = 60
        mic_height = 80
        mic_top = center_y - 50
        draw.rounded_rectangle(
            [center_x - mic_width//2, mic_top, 
             center_x + mic_width//2, mic_top + mic_height],
            radius=30,
            fill=(255, 255, 255, 255)
        )
        
        # 麦克风支架
        draw.rectangle(
            [center_x - 5, mic_top + mic_height, 
             center_x + 5, mic_top + mic_height + 30],
            fill=(255, 255, 255, 255)
        )
        
        # 麦克风底座
        draw.rounded_rectangle(
            [center_x - 40, mic_top + mic_height + 25,
             center_x + 40, mic_top + mic_height + 35],
            radius=5,
            fill=(255, 255, 255, 255)
        )
        
        # 保存为ICO格式
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save('icon.ico', format='ICO', sizes=icon_sizes)
        print("✓ 图标创建成功: icon.ico")
        
        # 同时保存PNG版本
        img.save('icon.png', format='PNG')
        print("✓ PNG图标创建成功: icon.png")
        
        return True
    
    if __name__ == "__main__":
        print("正在创建应用图标...")
        if os.path.exists('icon.ico'):
            response = input("icon.ico已存在，是否覆盖？(y/n): ")
            if response.lower() != 'y':
                print("取消创建")
                exit(0)
        
        create_icon()
        print("\n图标创建完成！")
        print("现在可以运行 build.bat 进行打包")

except ImportError:
    print("错误: 需要安装Pillow库")
    print("运行: pip install pillow")
    exit(1)
