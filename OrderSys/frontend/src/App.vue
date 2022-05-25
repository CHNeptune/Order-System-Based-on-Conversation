<template>
  <div id="app" style="width: 100%; height: 100%; position: absolute">
    <div
      style="
        width: 100%;
        height: 100%;
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
      "
      v-if="!showuser"
    >
      <img :src="imgbeginner" alt="快语订餐" />
    </div>

    <mu-fade-transition>
      <div v-if="showuser"><user /></div>
    </mu-fade-transition>
  </div>
</template>

<script>
import HelloWorld from "./components/HelloWorld";
import user from "./components/user.vue";

export default {
  name: "App",
  data() {
    return {
      showuser: false,
      imgbeginner: require("./assets/logo.png"),
    };
  },
  components: {
    HelloWorld,
    user,
  },
  methods: {
    show_user() {
      this.showuser = true;
      return;
    },
  },
  mounted() {
    setTimeout(this.show_user, 2000);
  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#showuser {
  position: absolute;
  bottom: 0;
}
</style>
