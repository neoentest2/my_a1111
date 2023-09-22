# Link all files by filtering accoridng to their type
with capture.capture_output() as cap:
  # files = os.listdir(destination_dir)
  files = [os.path.join(dp,f) for dp, dn, fn in os.walk(destination_dir) for f in fn] # Thanks Aojiru!
  for file in files:
    name, file_extension = os.path.splitext(file)
    if '.aria2' in file:
      continue
    file_path = os.path.join(destination_dir, file)
    file_size = os.path.getsize(file_path)
    if "sam_" in name and file_extension == ".pth":
      !ln "{file_path}" {sam_dir}
    elif "control_" in name or "t2iadapter_" in name or file_extension == ".pth":
      !ln "{file_path}" {control_dir}
    elif file_extension in ['.yaml', '.yml'] or file_size > 1_500_000_000:
      !ln "{file_path}" {models_dir}
    elif "kl-f8" in name or "vae_" in file or "vae." in file or "vae-" in file or file_size > 380_000_000:
      !ln "{file_path}" {vaes_dir}
    elif getoutput('if rg -q -o "lora_unet" "'+file_path+'"; then echo 1; else echo 0; fi') == "1":
      !ln "{file_path}" {loras_dir}
    elif (file_extension == '.pt' or file_extension == '.safetensors') and file_size < 10_000_000:
      !ln "{file_path}" {embeddings_dir}
    else:
      !ln "{file_path}" {hypernetworks_dir}
  del cap
