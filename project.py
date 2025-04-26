import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk


def apply_filter(image, filter_type):
    if filter_type == "none":
        return image
    elif filter_type == "Mean Filter":  
        return cv2.blur(image, (5, 5))
    elif filter_type == "Gaussian Filter":
        return cv2.GaussianBlur(image, (5, 5), 0)
    elif filter_type == "Median Filter":
        return cv2.medianBlur(image, 5)
    elif filter_type == "Bilateral Filter":
        return cv2.bilateralFilter(image, 9, 75, 75)
    elif filter_type == "Unsharp Masking":
        gaussian = cv2.GaussianBlur(image, (5, 5), 10.0)
        return cv2.addWeighted(image, 1.5, gaussian, -0.5, 0)
    elif filter_type == "Non-Local Means Denoising":
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    else:
        return image


def apply_edge_detection(image, edge_type):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if edge_type == "none":
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif edge_type == "Sobel Operator":
        edge = cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=5)
    elif edge_type == "Prewitt Operator":
        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernely = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
        edge = cv2.filter2D(gray, -1, kernelx) + cv2.filter2D(gray, -1, kernely)
    elif edge_type == "Laplacian Operator":
        edge = cv2.Laplacian(gray, cv2.CV_64F)
    elif edge_type == "Canny Edge Detector":
        edge = cv2.Canny(gray, 50, 150)
        return cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    elif edge_type == "Roberts Operator":
        kernelx = np.array([[1, 0], [0, -1]])
        kernely = np.array([[0, 1], [-1, 0]])
        edge = cv2.filter2D(gray, -1, kernelx) + cv2.filter2D(gray, -1, kernely)
    elif edge_type == "Scharr Operator":
        edge = cv2.Scharr(gray, cv2.CV_64F, 1, 0) + cv2.Scharr(gray, cv2.CV_64F, 0, 1)
    else:
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    edge = np.abs(edge)
    edge = np.uint8(edge)
    return cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)


def apply_transformation(image, transform_type):
    rows, cols = image.shape[:2]
    if transform_type == "none":
        return image
    elif transform_type == "Scaling":
        return cv2.resize(image, (cols * 2, rows * 2))
    elif transform_type == "Rotation":
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 45, 1)
        return cv2.warpAffine(image, M, (cols, rows))
    elif transform_type == "Translation":
        M = np.float32([[1, 0, 50], [0, 1, 50]])
        return cv2.warpAffine(image, M, (cols, rows))
    elif transform_type == "Shearing":
        M = np.float32([[1, 0.5, 0], [0.5, 1, 0]])
        return cv2.warpAffine(image, M, (cols, rows))
    elif transform_type == "Reflection":
        return cv2.flip(image, 1)
    elif transform_type == "Affine Transformation":
        pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
        pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
        M = cv2.getAffineTransform(pts1, pts2)
        return cv2.warpAffine(image, M, (cols, rows))
    elif transform_type == "Perspective Transformation":
        pts1 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
        pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        return cv2.warpPerspective(image, M, (300, 300))
    elif transform_type == "Log Transformation":
        c = 255 / np.log(1 + np.max(image))
        log_image = c * np.log(1 + image.astype(np.float32))
        log_image = np.uint8(log_image)
        return log_image
    elif transform_type == "Gamma Transformation":
        gamma = 2.2 
        c = 1
        gamma_corrected = c * np.power(image / 255.0, gamma)
        gamma_corrected = np.uint8(gamma_corrected * 255)
        return gamma_corrected
    elif transform_type == "Fourier Tranformation":
        f = np.fft.fft2(image)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = np.log(np.abs(fshift) + 1)

        magnitude_spectrum = np.abs(magnitude_spectrum)
        magnitude_spectrum = np.uint8(magnitude_spectrum * 255.0 / np.max(magnitude_spectrum)) 
        return magnitude_spectrum
    else:
        return image


def process_image():
    global image
    img = image.copy()
    img = apply_filter(img, filter_var.get())
    img = apply_edge_detection(img, edge_var.get())
    img = apply_transformation(img, transform_var.get())

    display_image(img, output_canvas)
    processed_images["output"] = img


def upload_image():
    global image
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        image = img
        display_image(img, input_canvas)
        processed_images["input"] = img


def display_image(img, canvas):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil = img_pil.resize((300, 300))
    imgtk = ImageTk.PhotoImage(image=img_pil)
    canvas.imgtk = imgtk
    canvas.create_image(0, 0, anchor='nw', image=imgtk)



app = tk.Tk()
app.title("✨ Image Processing App ✨")
app.geometry("1000x600")
app.configure(bg="#2b2b2b")

style = ttk.Style()
style.configure('TButton', 
                font=('Helvetica', 10, 'bold'),
                padding=10,
                background='#4a90e2',
                foreground='white')
style.configure('TLabel',
                font=('Helvetica', 10),
                background='#2b2b2b',
                foreground='white')
style.configure('TMenubutton',
                font=('Helvetica', 10),
                background='#3c3c3c',
                foreground='white')

image = None
processed_images = {}

filter_var = tk.StringVar(value="none")
edge_var = tk.StringVar(value="none")
transform_var = tk.StringVar(value="none")

main_frame = tk.Frame(app, bg="#2b2b2b")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

control_frame = tk.Frame(main_frame, bg="#2b2b2b")
control_frame.pack(side="left", fill="y", padx=(0, 20))


title_label = tk.Label(control_frame, 
                      text="Image Processing App",
                      font=("Helvetica", 16, "bold"),
                      bg="#2b2b2b",
                      fg="#4a90e2")
title_label.pack(pady=(0, 20))

upload_btn = tk.Button(control_frame,
                      text="📂 Upload Image",
                      command=upload_image,
                      bg="#4a90e2",
                      fg="white",
                      font=("Helvetica", 12, "bold"),
                      relief="flat",
                      padx=20,
                      pady=10)
upload_btn.pack(fill="x", pady=(0, 20))

filter_label = tk.Label(control_frame,
                       text="Select Filter",
                       font=("Helvetica", 10, "bold"),
                       bg="#2b2b2b",
                       fg="#ffffff")
filter_label.pack(anchor="w", pady=(0, 5))
filter_menu = ttk.OptionMenu(control_frame, filter_var, "none", "Mean Filter", "Gaussian Filter", "Median Filter",
                            "Bilateral Filter", "Unsharp Masking", "Non-Local Means Denoising")
filter_menu.pack(fill="x", pady=(0, 15))

edge_label = tk.Label(control_frame,
                     text="Select Edge Detection",
                     font=("Helvetica", 10, "bold"),
                     bg="#2b2b2b",
                     fg="#ffffff")
edge_label.pack(anchor="w", pady=(0, 5))
edge_menu = ttk.OptionMenu(control_frame, edge_var, "none", "Sobel Operator", "Prewitt Operator", "Laplacian Operator",
                          "Canny Edge Detector", "Roberts Operator", "Scharr Operator")
edge_menu.pack(fill="x", pady=(0, 15))

transform_label = tk.Label(control_frame,
                         text="Select Transformation",
                         font=("Helvetica", 10, "bold"),
                         bg="#2b2b2b",
                         fg="#ffffff")
transform_label.pack(anchor="w", pady=(0, 5))
transform_menu = ttk.OptionMenu(control_frame, transform_var, "none", "Scaling", "Rotation", "Translation", "Shearing",
                              "Reflection", "Affine Transformation", "Perspective Transformation","Fourier Tranformation", "Log Transformation","Gamma Transformation")
transform_menu.pack(fill="x", pady=(0, 15))

process_btn = tk.Button(control_frame,
                       text="🚀 Apply Processing",
                       command=process_image,
                       bg="#4a90e2",
                       fg="white",
                       font=("Helvetica", 12, "bold"),
                       relief="flat",
                       padx=20,
                       pady=10)
process_btn.pack(fill="x", pady=(20, 0))

image_frame = tk.Frame(main_frame, bg="#2b2b2b")
image_frame.pack(side="right", fill="both", expand=True)
input_frame = tk.Frame(image_frame, bg="#2b2b2b")
input_frame.pack(side="left", fill="both", expand=True, padx=10)

input_label = tk.Label(input_frame,
                      text="Original Image",
                      font=("Helvetica", 12, "bold"),
                      bg="#2b2b2b",
                      fg="#ffffff")
input_label.pack(pady=(0, 10))

input_canvas = tk.Canvas(input_frame, width=300, height=300, bg='#3c3c3c', highlightthickness=0)
input_canvas.pack()

output_frame = tk.Frame(image_frame, bg="#2b2b2b", width=300, height=300)
output_frame.pack(side="right", fill="both", expand=True, padx=10)

output_label = tk.Label(output_frame,
                       text="Processed Image",
                       font=("Helvetica", 12, "bold"),
                       bg="#2b2b2b",
                       fg="#ffffff")
output_label.pack(pady=(0, 10))

output_canvas = tk.Canvas(output_frame, width=300, height=300, bg='#3c3c3c', highlightthickness=0)
output_canvas.pack()

app.mainloop()