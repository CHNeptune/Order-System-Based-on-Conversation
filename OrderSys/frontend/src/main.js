// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import MuseUI from "muse-ui"
import "muse-ui/dist/muse-ui.css"
import Toast from 'muse-ui-toast';
import Message from 'muse-ui-message';
import 'muse-ui-loading/dist/muse-ui-loading.css'; // load css

import Loading from 'muse-ui-loading';

// import Vconsole from 'vconsole';
//  new Vconsole();
const ToastOption = {
  position: 'top', // 弹出的位置
  time: 2000, // 显示的时长
  closeIcon: 'close', // 关闭的图标
  close: false, // 是否显示关闭按钮
  successIcon: 'check_circle', // 成功信息图标
  infoIcon: 'info', // 信息信息图标
  warningIcon: 'priority_high', // 提醒信息图标
  errorIcon: 'warning' // 错误信息图标
}
Vue.use(Loading);
Vue.use(Message);
Vue.use(MuseUI);
Vue.use(Toast,ToastOption);
Vue.config.productionTip = false
document.body.style.overflow='hidden';
// var mo=function(e){
//   e.preventDefault()
// };
// document.addEventListener("touchmove",mo,false);//禁止页面滑动
/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>',
  
})
