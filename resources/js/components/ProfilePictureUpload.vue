<template>
  <div class="image-cropper-container">
    <h2>Upload and Crop Your Profile Picture</h2>

    <!-- Image Upload -->
    <input type="file" @change="onFileChange" accept="image/*" />

    <!-- Vue Cropper Component -->
    <vue-cropper 
      v-if="imageUrl" 
      :src="imageUrl"
      :aspect-ratio="1" 
      :auto-crop-area="0.8"
      :view-mode="1"
      ref="cropper"
    />
    
    <!-- Crop Button -->
    <div v-if="imageUrl">
      <button @click="submitImage">Submit Image</button>
    </div>

    <!-- Cropped Image Preview -->
    <div v-if="croppedImageUrl">
      <h3>Cropped Image</h3>
      <img :src="croppedImageUrl" alt="Cropped Profile Picture" />
    </div>
  </div>
</template>

<script>
import { vueCropper } from 'vue-cropperjs'; // Import vue-cropperjs
import "vue-cropperjs/node_modules/cropperjs/dist/cropper.css";
import axios from 'axios';

export default {
  components: {
    vueCropper, // Register the vue-cropper component
  },
  data() {
    return {
      imageUrl: null,
      croppedImageUrl: null,
      croppedImage:null
    };
  },
  methods: {
    // Method to handle file selection and load the image
    onFileChange(event) {
      const file = event.target.files[0];
        this.croppedImage = file;
    //   if (file) {
    //     const reader = new FileReader();
    //     reader.onload = (e) => {
          this.imageUrl = URL.createObjectURL(file);
    //       // Initialize the cropper once the image is loaded
    //       this.$nextTick(() => {        
    //         this.initializeCropper(); // Initialize cropper after DOM updates
    //       });
    //     };
    //     reader.readAsDataURL(file);
    //   }
    },

    // Method to initialize the cropper
    initializeCropper() {
      const cropper = this.$refs.cropper;
      console.log(cropper);
      
      if (cropper) {
        // This is where you can modify additional settings for the cropper
      }
    },

    // Method to crop the image
    submitImage() {
      const cropper = this.$refs.cropper;
      const uploadimage = '/upload-profile-picture'

      const formData = new FormData();
      formData.append('image',this.croppedImage);
      axios.post(uploadimage, formData)
        .then(response => {
        //   this.modelLoading = false;
        //   this.modelSucess = true;
        console.log(response);
        
        })
        .catch(error => {
        //   if (error.response) {
        //     // if (error.response.status === 422) {
        //     //   this.errorMassages = error.response.data.errors;
        //     // } else if (error.response.status === 413) {
        //     //   this.errorMassages = [['The file you are trying to upload is too large. Please select a smaller file.']];
        //     // } else if (error.response.data?.errors?.message) {
        //     //   this.errorMassages = [[error.response.data.errors.message]];
        //     // } else {
        //     //   this.errorMassages = [['An error occurred while saving the media.']];
        //     // }
        //   } else {
        //     // this.errorMassages = [['A network error occurred. Please try again.']];
        //   }

        //   this.modelLoading = false;
        });
    },
  },
};
</script>

<style scoped>
.image-cropper-container {
  text-align: center;
  padding: 20px;
}

button {
  margin-top: 20px;
  padding: 10px;
  font-size: 16px;
}

img {
  max-width: 100%;
  margin-top: 20px;
}
</style>
