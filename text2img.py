from diffusers import (
    AutoPipelineForText2Image,
    StableDiffusionXLPipeline,
    AutoencoderTiny,
    AutoencoderKL,
    KDPM2AncestralDiscreteScheduler
)
import torch
import gc 

vae = AutoencoderKL.from_pretrained(
    "madebyollin/sdxl-vae-fp16-fix", 
    torch_dtype=torch.float16
)
def generate(prompt,negative_prompt,num_inference_steps):
    pipeline_text2image = AutoPipelineForText2Image.from_pretrained(
#   "stabilityai/stable-diffusion-xl-base-1.0", #base model 
#   "segmind/SSD-1B", #smaller model of SDXL, reduce 40% weight and size, increase inference time
#   "segmind/Segmind-Vega", #Reduce 60% weight and size, increase 100% inference time
#   "dataautogpt3/OpenDalleV1.1", #best quality model, but the inference time is long
	"dataautogpt3/ProteusV0.4",
    vae=vae,
    cache_dir="/home/www/data/data/saigonmusic/Dev_AI/thainh/cache_huggingface", 
    torch_dtype=torch.float16, 
#   variant="fp16", 
#   use_safetensors=True
    )
    pipeline_text2image.scheduler = KDPM2AncestralDiscreteScheduler.from_config(pipeline_text2image.scheduler.config)
    pipeline_text2image.to("cuda")
    # pipeline_text2image.enable_freeu(b1= 1.3, b2=1.4, s1=0.9, s2=0.2)

    for word in prompt.split(" "):
        if word=="cartoon" or word=="Cartoon":
            pipeline_text2image.load_lora_weights("/home/www/data/data/saigonmusic/Dev_AI/thainh/LoRA",weight_name="SDXL_cartoon_1500.safetensors")
        if word=="christmas" or word=="Christmas":
            pipeline_text2image.load_lora_weights("/home/www/data/data/saigonmusic/Dev_AI/thainh/LoRA", weight_name="SDXL-2000-christmas.safetensors")
        if word=="art" or word=="Art":
            pipeline_text2image.load_lora_weights("/home/www/data/data/saigonmusic/Dev_AI/thainh/LoRA",weight_name="SDXL_art_1500.safetensors")
            
    image = pipeline_text2image(prompt=prompt, negative_prompt=negative_prompt, num_inference_steps=num_inference_steps, guidance_scale=6, width=1024,
    height=1024, num_images_per_prompt=2).images[0]
    image.save("static/images/image1.png")
    
    del pipeline_text2image
    del image
    
    torch.cuda.empty_cache()
    gc.collect()
    
    # return image


if __name__ == "__main__":
    # prompt="black fluffy gorgeous dangerous cat animal creature, large orange eyes, big fluffy ears, piercing gaze, full moon, dark ambiance, best quality, extremely detailed, HD."
    # negative_prompt="nsfw, bad quality, bad anatomy, worst quality, low quality, low resolutions, extra fingers, blur, blurry, ugly, wrongs proportions, watermark, image artifacts, lowres, ugly, jpeg artifacts, deformed, noisy image"
    import json
    with open("info.json", "r") as f:
        json_data = json.load(f)
    prompt = json_data["prompt"]
    negative_prompt = json_data["negative_prompt"]
    num_inference_steps=60
    generate(prompt,negative_prompt,num_inference_steps)
    # đọc file json lấy thông tin và  thực hiện gen ảnh sau đó xoá file json đi