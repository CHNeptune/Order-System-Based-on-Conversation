<template>
  <div class="hello">
    <img src="../assets/logo.png">
    <h1>{{ msg }}</h1>
    
  </div>
</template>

<script>
import Vue from 'vue';
import MuseUI from 'muse-ui';
import 'muse-ui/dist/muse-ui.css';
Vue.use(MuseUI);
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
h1, h2 {
  font-weight: normal;
}
.mu-ripple-demo {
  position: relative;
  width: 200px;
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 16px;
  background-color: #fff;
  border-radius: 4px;

  &.demo-1 {
    color: #2196f3;
    border: 1px solid #2196f3;
  }
}
</style>
