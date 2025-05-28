<template>
  <div class="rich-text-editor">
    <div ref="editorContainer"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, defineProps, defineEmits } from 'vue';
import Quill from 'quill';
import 'quill/dist/quill.snow.css'; // or 'quill/dist/quill.bubble.css'

const props = defineProps({
  modelValue: { // for v-model
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '开始写作...'
  },
  readOnly: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'ready']);

const editorContainer = ref(null);
let quillInstance = null;

const toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
  ['blockquote', 'code-block'],

  [{ 'header': 1 }, { 'header': 2 }],               // custom button values
  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
  [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
  [{ 'direction': 'rtl' }],                         // text direction

  [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
  [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

  [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
  [{ 'font': [] }],
  [{ 'align': [] }],

  ['link', 'image', 'video'],                       // link, image, video
  ['clean']                                         // remove formatting button
];

onMounted(() => {
  if (editorContainer.value) {
    quillInstance = new Quill(editorContainer.value, {
      theme: 'snow', // 'snow' or 'bubble'
      modules: {
        toolbar: props.readOnly ? false : toolbarOptions
      },
      placeholder: props.placeholder,
      readOnly: props.readOnly,
    });

    // Set initial content if modelValue is provided
    if (props.modelValue) {
      // Quill's setContents expects a Delta object or HTML string.
      // If modelValue is HTML, it's better to use clipboard.dangerouslyPasteHTML.
      // For simplicity here, if it's plain text or simple HTML, this might work.
      // A safer way for HTML:
      // const delta = quillInstance.clipboard.convert(props.modelValue);
      // quillInstance.setContents(delta, 'silent');
      quillInstance.root.innerHTML = props.modelValue;
    }

    quillInstance.on('text-change', (delta, oldDelta, source) => {
      if (source === 'user') {
        // Get HTML content from Quill
        let html = quillInstance.root.innerHTML;
        // Quill sometimes adds <p><br></p> for empty content, normalize it
        if (html === '<p><br></p>') html = '';
        emit('update:modelValue', html);
      }
    });
    emit('ready', quillInstance);
  }
});

onBeforeUnmount(() => {
  if (quillInstance) {
    quillInstance.off('text-change');
    // Potentially destroy quill instance if library provides such method
  }
});

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  if (quillInstance && quillInstance.root.innerHTML !== newValue) {
    // quillInstance.setContents(quillInstance.clipboard.convert(newValue), 'silent');
    quillInstance.root.innerHTML = newValue || ''; // Set HTML directly
  }
});

watch(() => props.readOnly, (newVal) => {
  if (quillInstance) {
    quillInstance.enable(!newVal);
  }
});

</script>

<style scoped>
.rich-text-editor {
  min-height: 300px; /* Or whatever height you prefer */
  border: 1px solid #ccc;
  border-radius: 4px;
}
/* Quill's CSS will style the editor itself, ensure it's loaded */
/* You might need to adjust Quill's default styling or container height */
:deep(.ql-editor) {
    min-height: 250px; /* Example internal editor height */
}
</style>