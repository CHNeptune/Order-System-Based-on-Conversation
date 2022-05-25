<template>
  <div class="user">
    <mu-ripple class="mu-ripple-demo demo-1">
      <mu-appbar
        style="width: 100%; position: absolute; top: 0"
        color="primary"
      >
        <mu-menu :open.sync="menu" slot="left">
          <mu-icon
            value="menu"
            :size="40"
            style="margin-top: 8px; margin-left: 5px"
          ></mu-icon>
          <mu-list slot="content">
            <mu-list-item button>
              <mu-list-item-content>
                <mu-list-item-title>关于</mu-list-item-title>
              </mu-list-item-content>
            </mu-list-item>
            <mu-list-item button @click="logout()">
              <mu-list-item-content>
                <mu-list-item-title>退出登陆</mu-list-item-title>
              </mu-list-item-content>
            </mu-list-item>
          </mu-list>
        </mu-menu>
        快语订餐
        <mu-menu slot="right">
          <mu-button flat @click="open_history = !open_history"
            >对话历史</mu-button
          >
        </mu-menu>
      </mu-appbar>
      <div class="loading" style="z-index: 9999" v-if="load == 1">
        <mu-circular-progress
          class="demo-circular-progress"
          color="warning"
          :stroke-width="7"
          :size="56"
        ></mu-circular-progress>
      </div>

      <mu-drawer
        :open.sync="open_history"
        :docked="false"
        :right="true"
        :width="300"
        style="height: 85%; top: 10%"
      >
        <mu-icon
          @click="open_history = false"
          size="36"
          value="close"
          style="float: left"
        ></mu-icon>
      </mu-drawer>
      <div class="goods" style="width: 100%" v-if="now == 'goods'">
        <div v-if="uid == '-1'" style="font-size: 24px">
          <mu-icon value="warning" size="56"></mu-icon><br />登陆后即可查看
        </div>
        <div
          v-if="uid != '-1'"
          style="width: 100%; position: fixed; top: 7%; left: 0"
        >
          <mu-tabs
            inverse
            color="secondary"
            text-color="rgba(0, 0, 0, .54)"
            center
            style="overflow-x: auto"
            :value.sync="typeTab"
          >
            <mu-tab v-for="(each, index) in typeList" :key="index">{{
              each
            }}</mu-tab>
          </mu-tabs>
        </div>

        <div class="foodspage" v-if="uid != '-1'">
          <mu-flex justify-content="center">
            <mu-paper :z-depth="1" style="width: 98%">
              <mu-grid-list class="gridlist">
                <mu-grid-tile
                  v-for="(each, index) in foodsTypeList"
                  :key="index"
                >
                  <img
                    @click="showDetail(each)"
                    :src="'https://' + HOST + '/img?imgname=' + each.img"
                  />
                  <span slot="title">{{ each.name }}</span>
                  <span slot="subTitle"
                    ><b
                      >￥<span style="text-decoration: line-through">{{
                        each.old_price
                      }}</span
                      >&nbsp;￥{{ each.new_price }}</b
                    ></span
                  >
                  <mu-dialog title="详情" width="360" :open.sync="openDetail">
                    <div v-html="describe"></div>
                    <mu-button
                      slot="actions"
                      flat
                      color="primary"
                      @click="openDetail = !openDetail"
                      >关闭</mu-button
                    >
                    <mu-button
                      v-if="uname != 'BUSINESS'"
                      slot="actions"
                      flat
                      color="primary"
                      @click="
                        () => {
                          openDetail = !openDetail;
                          addIntoCart(fIDNow.toString());
                        }
                      "
                      >加入购物车</mu-button
                    >
                    <mu-button
                      v-if="uname == 'BUSINESS'"
                      slot="actions"
                      flat
                      color="primary"
                      @click="
                        () => {
                          openDetail = !openDetail;
                          foodDetail = !foodDetail;
                          UpdateOrAdd = 'update';
                          editFood(fIDNow);
                        }
                      "
                      >编辑</mu-button
                    >
                  </mu-dialog>
                  <mu-button
                    slot="action"
                    @click="addIntoCart(each.ID.toString())"
                    icon
                  >
                    <mu-icon value="star_border"></mu-icon>
                  </mu-button>
                </mu-grid-tile>
              </mu-grid-list>
            </mu-paper>
          </mu-flex>
          <div v-if="uname == 'BUSINESS'" style="padding: 10px">
            <mu-button
              round
              @click="
                () => {
                  foodDetail = !foodDetail;
                  UpdateOrAdd = 'add';
                  addFood();
                }
              "
              color="red"
            >
              <mu-icon size="36" value="add"></mu-icon>
            </mu-button>
          </div>
        </div>

        <mu-slide-bottom-transition>
          <div
            id="foodDetail"
            v-if="foodDetail"
            style="
              padding: 5%;
              position: fixed;
              z-index: 999;
              left: 1%;
              width: 98%;
              height: 92%;
              background: white;
              top: 5%;
            "
          >
            <mu-divider></mu-divider>
            <span style="text-align: center">商品详情</span><br />

            <mu-text-field
              style="width: 59%"
              v-model="foodDetailList.name"
              label="商品名"
              label-float
              help-text="6-12长度的字符"
            ></mu-text-field>
            <mu-text-field
              style="width: 39%"
              v-model="foodDetailList.type"
              label="商品类型"
              label-float
              help-text="6-12长度的字符"
            ></mu-text-field>

            <br />
            <mu-text-field
              style="width: 49%"
              v-model="foodDetailList.old_price"
              label="原价"
              label-float
              help-text="6-12长度的字符"
            ></mu-text-field>
            <mu-text-field
              style="width: 49%"
              v-model="foodDetailList.new_price"
              label="现价"
              label-float
              help-text="6-12长度的字符"
            ></mu-text-field
            ><br />
            <mu-text-field
              style="width: 98%"
              v-model="foodDetailList.introduce"
              label="介绍"
              label-float
              help-text="25字符以内"
            ></mu-text-field
            ><br />
            <span style="text-align: left; color: black">图像</span><br />
            <img style="height: 250px; width: 250px" :src="picShowNow" />
            <input
              @change="showPicChoosed()"
              id="img"
              type="file"
              accept="image/jpeg"
            />
            <mu-select v-model="foodDetailList.state" label="状态" label-float>
              <mu-option label="有效" :value="1">有效</mu-option>
              <mu-option label="无效" :value="0">无效</mu-option> </mu-select
            ><br />

            <mu-button
              v-if="uname == 'BUSINESS'"
              color="green"
              flat
              @click="updateFoodClicked(foodDetailList)"
            >
              <mu-icon left value="navigation"></mu-icon>
              提交
            </mu-button>
            <mu-button
              @click="foodDetail = !foodDetail"
              flat
              color="red"
              style="margin: 20px"
            >
              <mu-icon left value="close"></mu-icon>
              关闭
            </mu-button>

            <mu-divider></mu-divider>
          </div>
        </mu-slide-bottom-transition>
      </div>
      <div
        class="cart"
        style="width: 100%; height: 80%; position: absolute; top: 8%"
        v-if="now == 'cart'"
      >
        <div
          v-if="uid == '-1'"
          style="font-size: 24px; position: absolute; top: 44%; left: 29%"
        >
          <mu-icon value="warning" size="56"></mu-icon><br />登陆后即可查看
        </div>
        <div v-if="uid != '-1'" style="overflow-y: auto; display: inline">
          <div
            style="
              color: red;
              font-size: large;
              position: absolute;
              top: 0%;
              right: 10%;
            "
          >
            <mu-icon left color="blue" size="24" value="local_atm"> </mu-icon
            >共计{{ cartPrice }}元
          </div>
          <mu-paper
            style="
              width: 98%;
              overflow-y: auto;
              height: 80%;
              position: absolute;
              top: 5%;
            "
          >
            <mu-list textline="three-line">
              <mu-list-item
                v-for="(c, index) in cartList"
                :key="index"
                avatar
                :ripple="false"
                button
              >
                <mu-list-item-action>
                  <mu-avatar>
                    <img :src="'https://' + HOST + '/img?imgname=' + c.img" />
                  </mu-avatar>
                </mu-list-item-action>
                <mu-list-item-content>
                  <mu-list-item-title>{{ c.name }}</mu-list-item-title>
                  <mu-list-item-sub-title>
                    <span style="color: rgba(200, 0, 0, 0.87)">{{
                      c.new_price
                    }}</span>
                    {{ c.introduce }}
                  </mu-list-item-sub-title>
                </mu-list-item-content>
                <mu-list-item-action>
                  <mu-icon
                    class="buttons"
                    @click="addIntoCart(c.ID.toString())"
                    style="position: absolute; right: 25%; top: 25%"
                    value="add"
                  ></mu-icon>

                  <span style="position: absolute; right: 15%; top: 25%"
                    >{{ c.number }}份</span
                  >

                  <mu-icon
                    class="buttons"
                    @click="deleteFromCart(c.ID.toString())"
                    style="position: absolute; top: 25%; right: 5%"
                    value="remove"
                  ></mu-icon>
                </mu-list-item-action>
              </mu-list-item>

              <mu-divider></mu-divider>
            </mu-list>
          </mu-paper>
          <div style="position: absolute; top: 87%; right: 25%">
            <mu-button @click="clearCart()" flat color="red">
              清空
              <mu-icon right value="clear"></mu-icon>
            </mu-button>
            <mu-button @click="clickMakeOrder()" flat color="red">
              结账
              <mu-icon right value="send"></mu-icon>
            </mu-button>
          </div>
        </div>
      </div>
      <div
        class="dialogopt"
        style="
          width: 98%;
          height: 80%;
          position: absolute;
          top: 7%;
          overflow-y: auto;
        "
        v-if="now == 'dialogopt'"
      >
        <div
          v-if="uid == '-1'"
          style="font-size: 24px; position: absolute; top: 44%; left: 29%"
        >
          <mu-icon value="warning" size="56"></mu-icon><br />登陆后即可查看
        </div>
        <div v-if="uid != '-1'">
          <mu-list textline="two-line">
            <mu-list-item
              v-for="(msg, index) in msgList"
              :key="index"
              avatar
              button
              :ripple="false"
            >
              <mu-list-item-action>
                <mu-avatar>
                  <mu-icon
                    v-if="msg.isread == 0"
                    color="red"
                    value="message"
                  ></mu-icon>
                  <mu-icon v-if="msg.isread == 1" value="message"></mu-icon>
                </mu-avatar>
              </mu-list-item-action>
              <mu-list-item-content>
                <mu-list-item-title v-if="msg.isread == 0" style="color: red"
                  >{{ msg.title
                  }}<span style="color: grey; font-size: small"
                    >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{ msg.date }}</span
                  ></mu-list-item-title
                >
                <mu-list-item-title v-if="msg.isread == 1"
                  >{{ msg.title
                  }}<span style="color: grey; font-size: small"
                    >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{ msg.date }}</span
                  ></mu-list-item-title
                >
                <mu-list-item-sub-title>{{
                  msg.content
                }}</mu-list-item-sub-title>
              </mu-list-item-content>
              <mu-list-item-action>
                <mu-button @click="alreadyRead(msg.ID)" icon>
                  <mu-icon value="done"></mu-icon>
                </mu-button>
              </mu-list-item-action>
            </mu-list-item>
          </mu-list>
        </div>
      </div>
      <div class="mine" v-if="now == 'mine'">
        <mu-slide-bottom-transition>
          <div
            id="registerPage"
            v-if="registerOpen"
            style="
              padding: 5%;
              position: fixed;
              z-index: 999;
              left: 1%;
              width: 98%;
              height: 65%;
              background: white;
            "
          >
            新用户注册<br />
            <mu-text-field
              v-model="register.name"
              label="姓名"
              label-float
            ></mu-text-field
            ><br />
            <mu-text-field
              v-model="register.address"
              label="地址"
              label-float
            ></mu-text-field
            ><br />
            <mu-text-field
              v-model="register.phone"
              label="电话"
              label-float
            ></mu-text-field
            ><br />
            <mu-text-field
              v-model="register.uname"
              label="注册用户名"
              label-float
            ></mu-text-field
            ><br />
            <mu-text-field
              v-model="register.passwd"
              label="注册密码"
              :action-icon="
                register.visibility ? 'visibility_off' : 'visibility'
              "
              :action-click="() => (register.visibility = !register.visibility)"
              :type="register.visibility ? 'text' : 'password'"
              label-float
            ></mu-text-field
            ><br />
            <mu-text-field
              v-model="register.confirmpwd"
              label="确认密码"
              :action-icon="
                register.visibility ? 'visibility_off' : 'visibility'
              "
              :action-click="() => (register.visibility = !register.visibility)"
              :type="register.visibility ? 'text' : 'password'"
              label-float
            ></mu-text-field
            ><br />

            <div
              style="
                width: 100%;
                height: 10%;
                font-size: large;
                text-align: right;
              "
            >
              <mu-button @click="registerNow()" flat color="red">
                <mu-icon left value="priority_high"></mu-icon>
                注册
              </mu-button>
              <mu-button @click="registerOpen = !registerOpen" flat color="red">
                <mu-icon left value="close"></mu-icon>
                关闭
              </mu-button>
            </div>
            <mu-divider></mu-divider>
          </div>
        </mu-slide-bottom-transition>
        <mu-slide-bottom-transition>
          <div
            id="orderDetail"
            v-if="orderDetailOpen"
            style="
              padding: 5%;
              position: fixed;
              z-index: 999;
              left: 1%;
              width: 98%;
              height: 82%;
              background: white;
            "
          >
            <mu-divider></mu-divider>
            订单详情
            <div
              style="
                width: 100%;
                height: 5%;
                font-size: large;
                text-align: left;
              "
            >
              <mu-icon value="done_outline"></mu-icon> 订单号:
              <span style="color: black">{{ theOrder.ID }}</span>
            </div>

            <mu-list style="height: 45%; overflow-y: auto">
              <mu-list-item
                v-for="(f, index) in orderFoodsList"
                :key="index"
                button
              >
                <mu-icon value="arrow_forward"></mu-icon>
                <mu-list-item-title>{{ f.name }}</mu-list-item-title>
                <mu-list-item-sub-title
                  >￥<span style="color: red"> {{ f.new_price }}</span>
                  <span style="text-align: right"> X {{ f.number }}</span>
                </mu-list-item-sub-title>
              </mu-list-item>
            </mu-list>
            <div
              style="
                width: 100%;
                height: 5%;
                font-size: large;
                text-align: left;
              "
            >
              <mu-icon value="timer"></mu-icon>下单时间:
              <span style="color: black">{{ theOrder.date }}</span>
            </div>
            <div
              style="
                width: 100%;
                height: 9%;
                font-size: large;
                text-align: left;
              "
            >
              <mu-icon value="360"></mu-icon>备注:
              <span style="color: black">{{ theOrder.remark }}</span>
            </div>
            <div
              style="
                width: 100%;
                height: 6%;
                font-size: large;
                text-align: left;
                margin-left: 46%;
              "
            >
              <mu-icon value="near_me"></mu-icon>总价:
              <span style="color: orange">￥{{ theOrder.price }}</span>
            </div>
            <div
              style="
                width: 100%;
                height: 20%;
                font-size: medium;
                text-align: right;
              "
            >
              <mu-button
                v-if="uname != 'BUSINESS'"
                flat
                color="red"
                style="margin: 20px"
              >
                <mu-icon left value="priority_high"></mu-icon>
                撤销订单
              </mu-button>
              <mu-button
                @click="getUserInformation(theOrder.uid)"
                v-if="uname == 'BUSINESS'"
                color="blue"
              >
                查看用户
              </mu-button>
              <mu-button
                v-if="uname == 'BUSINESS'"
                color="green"
                @click="orderSet_1Clicked()"
              >
                {{ orderSet.set1 }}
              </mu-button>
              <mu-button
                v-if="uname == 'BUSINESS'"
                color="green"
                @click="orderSet_2Clicked()"
              >
                {{ orderSet.set2 }}
              </mu-button>
              <mu-button
                @click="orderDetailOpen = !orderDetailOpen"
                flat
                color="red"
                style="margin: 20px"
              >
                <mu-icon left value="close"></mu-icon>
                关闭
              </mu-button>
              <span
                v-if="tempUserData.showUserData"
                style="text-align: left;position: absolute; left: 10px"
                >名字: {{ tempUserData.name }} <br />用户名: {{
                  tempUserData.uname
                }}
                <br />桌号: {{ tempUserData.table_number }}</span
              >
            </div>
            <mu-divider></mu-divider>
          </div>
        </mu-slide-bottom-transition>

        <mu-expand-transition style="margin: auto; margin-top: 10%">
          <div v-if="uid == '-1'">
            <div
              class="icon-container"
              style="margin-bottom: 12px; text-align: center"
            >
              <mu-icon size="130" value="send"></mu-icon><br />
              您还未登录，登陆后即可点餐~
            </div>
            <mu-container>
              <mu-form
                ref="form"
                :model="validateForm"
                class="mu-demo-form"
                style="width: 65%; margin: auto"
              >
                <mu-form-item
                  label="用户名"
                  help-text="您的注册账号"
                  prop="username"
                  :rules="usernameRules"
                >
                  <mu-text-field
                    v-model="validateForm.username"
                    prop="username"
                  ></mu-text-field>
                </mu-form-item>
                <mu-form-item
                  label="密码"
                  prop="password"
                  :rules="passwordRules"
                >
                  <mu-text-field
                    type="password"
                    v-model="validateForm.password"
                    prop="password"
                  ></mu-text-field>
                </mu-form-item>
                <mu-form-item prop="isAgree" :rules="argeeRules">
                  <mu-checkbox
                    label="同意用户协议"
                    v-model="validateForm.isAgree"
                  ></mu-checkbox>
                  <div
                    id="aggrement"
                    style="text-decoration: underline"
                    @click="show_aggrement()"
                  >
                    用户协议
                  </div>
                </mu-form-item>
                <mu-form-item>
                  <mu-button color="primary" @click="submit">登陆</mu-button>
                  <mu-button @click="registerOpen = !registerOpen"
                    >注册</mu-button
                  >
                </mu-form-item>
              </mu-form>
            </mu-container>
          </div>
        </mu-expand-transition>

        <div v-if="uid != '-1'" class="mine-login">
          <div class="personal" style="height: 25%">
            <mu-card style="width: 100%; max-width: 375px; margin: 0 auto">
              <div style="width: 100%; height: 70px">
                <mu-card-header
                  style="float: left"
                  :title="uname"
                  sub-title="HI"
                >
                  <mu-avatar slot="avatar">
                    <img src="../assets/logo.png" />
                  </mu-avatar>
                </mu-card-header>
              </div>

              <div style="width: 100%; height: 105px; padding: 5px">
                <span
                  style="
                    color: grey;
                    font-size: small;
                    left: 0;
                    position: absolute;
                    padding-top: 14px;
                    padding-left: 5px;
                  "
                  >电话</span
                >
                <mu-text-field
                  :disabled="true"
                  style="
                    width: 50%;
                    display: block;
                    position: absolute;
                    top: 76px;
                    padding-left: 10%;
                  "
                  v-model="phone"
                  type="number"
                  :solo="true"
                ></mu-text-field>
                <mu-icon
                  class="editicon"
                  style="position: absolute; top: 87px; left: 45%"
                  @click="changes('phone')"
                  size="20"
                  value="edit"
                ></mu-icon>
                <span
                  style="
                    color: grey;
                    font-size: small;
                    left: 0;
                    position: absolute;
                    padding-top: 56px;
                    padding-left: 5px;
                  "
                  >桌号</span
                >
                <mu-text-field
                  :disabled="true"
                  style="
                    width: 50%;
                    display: block;
                    position: absolute;
                    top: 118px;
                    padding-left: 10%;
                  "
                  v-model="table_number"
                  type="number"
                  :solo="true"
                ></mu-text-field>
                <mu-icon
                  class="editicon"
                  style="position: absolute; top: 129px; left: 45%"
                  @click="changes('table_number')"
                  size="20"
                  value="edit"
                ></mu-icon>
              </div>
            </mu-card>
          </div>
          <div class="options">
            <mu-list toggle-nested>
              <mu-list-item
                button
                nested
                :open="panel === 'order'"
                @toggle-nested="toggle('order')"
                @click="getAllOrder()"
              >
                <mu-list-item-action>
                  <mu-icon value="filter_none"></mu-icon>
                </mu-list-item-action>
                <mu-list-item-title v-if="uname != 'BUSINESS'"
                  >我的订单</mu-list-item-title
                >
                <mu-list-item-title v-if="uname == 'BUSINESS'"
                  >用户订单</mu-list-item-title
                >
                <mu-list-item-action>
                  <mu-icon
                    class="toggle-icon"
                    value="keyboard_arrow_down"
                  ></mu-icon>
                </mu-list-item-action>
                <mu-list-item slot="nested" button :ripple="true">
                  <mu-tabs
                    :value.sync="order_active_page"
                    color="rgba(20,60,120,.5)"
                    indicator-color="yellow"
                    style="position: absolute; left: 0"
                    full-width
                  >
                    <mu-tab v-if="uname != 'BUSINESS'">全部</mu-tab>
                    <mu-tab v-if="uname == 'BUSINESS'">无效</mu-tab>
                    <mu-tab>待支付</mu-tab>
                    <mu-tab>待服务</mu-tab>
                    <mu-tab>已完成</mu-tab>
                  </mu-tabs>
                </mu-list-item>

                <div style="height: 300px; overflow-y: auto" slot="nested">
                  <mu-list>
                    <mu-list-item
                      v-for="(order, index) in orderList"
                      :key="index"
                      button
                      @click="showOrder(order)"
                    >
                      <mu-icon value="event_note"></mu-icon>
                      <mu-list-item-title style="width: 150%">
                        {{ order.date }}</mu-list-item-title
                      >
                      <mu-list-item-sub-title style="color: red">
                        ￥{{ order.price }}
                      </mu-list-item-sub-title>
                    </mu-list-item>
                  </mu-list>
                </div>
              </mu-list-item>
              <mu-list-item
                button
                nested
                :open="panel === 'dsetting'"
                @toggle-nested="toggle('dsetting')"
              >
                <mu-list-item-action>
                  <mu-icon value="settings"></mu-icon>
                </mu-list-item-action>
                <mu-list-item-title>对话设置</mu-list-item-title>
                <mu-list-item-action>
                  <mu-icon
                    class="toggle-icon"
                    value="keyboard_arrow_down"
                  ></mu-icon>
                </mu-list-item-action>

                <!-- <mu-sub-header>自动对话</mu-sub-header> -->
                <mu-list-item
                  slot="nested"
                  button
                  :ripple="true"
                  @click="auto_listen = !auto_listen"
                >
                  <mu-list-item-title style="width: 50%"
                    >连续对话</mu-list-item-title
                  >
                  <mu-list-item-sub-title style="text-align: left"
                    >环境嘈杂时不建议开启</mu-list-item-sub-title
                  >
                  <mu-list-item-action>
                    <mu-switch v-model="auto_listen" readonly></mu-switch>
                  </mu-list-item-action>
                </mu-list-item>
              </mu-list-item>
              <mu-list-item
                button
                nested
                :open="panel === 'ssetting'"
                @toggle-nested="toggle('ssetting')"
              >
                <mu-list-item-action>
                  <mu-icon value="settings"></mu-icon>
                </mu-list-item-action>
                <mu-list-item-title>系统设置</mu-list-item-title>
                <mu-list-item-action>
                  <mu-icon
                    class="toggle-icon"
                    value="keyboard_arrow_down"
                  ></mu-icon>
                </mu-list-item-action>

                <!-- <mu-sub-header>自动对话</mu-sub-header> -->
                <mu-list-item
                  slot="nested"
                  button
                  :ripple="true"
                  @click="changePwd()"
                >
                  <mu-list-item-title style="width: 50%"
                    >修改密码</mu-list-item-title
                  >
                </mu-list-item>
              </mu-list-item>
              <!-- TDOD:四个类型订单显示 -->
            </mu-list>
          </div>
        </div>
      </div>

      <div class="voice" style="color: #2196f3">
        <mu-container
          style="float: left; width: 90px; position: fixed; bottom: 10%"
          class="button-wrapper"
        >
          <mu-button
            large
            fab
            color="rgba(180,0,120,.8)"
            data-mu-loading-overlay-color="rgba(90, 90, 90, .5)"
            v-loading="vload"
            @click="voice_clicked()"
          >
            <mu-icon :value="mic"></mu-icon>
          </mu-button>
        </mu-container>
        <div class="text_area">
          <div v-for="d in dialog_message_list" v-bind:key="d">
            <mu-slide-bottom-transition :appear="true">
              <div v-show="true">
                {{ d }}
              </div>
            </mu-slide-bottom-transition>
          </div>
        </div>
      </div>

      <div class="buttom" @click="shift()">
        <mu-container style="padding-right: 0px; padding-left: 0px">
          <mu-bottom-nav :value.sync="now" shift>
            <mu-bottom-nav-item
              value="goods"
              title="商品"
              icon="restaurant"
            ></mu-bottom-nav-item>
            <mu-bottom-nav-item
              value="cart"
              title="购物车"
              icon="star_border"
            ></mu-bottom-nav-item>
            <mu-bottom-nav-item
              value="dialogopt"
              title="消息"
              icon="notifications"
            ></mu-bottom-nav-item>
            <mu-bottom-nav-item
              value="mine"
              title="个人中心"
              icon="home"
            ></mu-bottom-nav-item>
          </mu-bottom-nav>
        </mu-container>
      </div>
    </mu-ripple>
  </div>
</template>

<script>
import Recorder from "js-audio-recorder";
import axios from "axios";
var HOST = "121.36.111.79:4999";
export default {
  name: "user",
  data() {
    return {
      uid: "-1",
      auto_listen: true, //自动开启下一轮对话
      uname: "NULL",
      phone: "00000000000",
      table_number: "2",
      cookie_of_uid: "-1",
      foodsList: [],
      foodsTypeList: [],
      typeList: [],
      cartList: [],
      orderList: [],
      theOrder: [],
      orderFoodsList: [],
      cartPrice: 0.0,
      remark: "",
      orderDetailOpen: false,
      registerOpen: false,
      register: {
        name: "",
        addresss: "",
        phone: "",
        uname: "",
        passwd: "",
        confirmpwd: "",
        visibility: false,
      },
      msg: "This is user UI",
      now: "mine",
      mic: "mic_none",
      dialog_message_list: [],
      user_text: "",
      orderSet: {
        set1: "设置无效",
        set2: "设置完成",
      },
      recorder: new Recorder({
        sampleBits: 16, // 采样位数，支持 8 或 16，默认是16
        sampleRate: 16000, // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
        numChannels: 1, // 声道，支持 1 或 2， 默认是1

        error: function (msg) {
          //失败回调函数
          alert(msg);
        },
        fix: function (msg) {
          //不支持H5录音回调函数
          alert(msg);
        },
      }),

      usernameRules: [
        { validate: (val) => !!val, message: "必须填写用户名" },
        { validate: (val) => val.length >= 3, message: "用户名长度大于3" },
      ],
      passwordRules: [
        { validate: (val) => !!val, message: "必须填写密码" },
        {
          validate: (val) => val.length >= 3 && val.length <= 10,
          message: "密码长度大于3小于10",
        },
      ],
      argeeRules: [{ validate: (val) => !!val, message: "必须同意用户协议" }],
      validateForm: {
        username: "",
        password: "",
        isAgree: false,
      },
      load: 0,
      menu: false,
      hand_end: false,
      voice_arr: new Array(),
      timer: 0,
      open_history: false,
      panel: "",
      StartAudio: new Audio(require("../assets/WindowsDing.wav")),
      MsgAudio: new Audio(require("../assets/WindowsError.wav")),
      vload: false,
      phoneCanChange: true,
      order_active_page: 2,
      typeTab: 0,
      openDetail: false,
      describe: "",
      msgList: [],
      foodDetail: false,
      foodDetailList: {
        id: -1,
        name: "name",
        type: "type",
        old_price: "old_price",
        new_price: "new_price",
        introduce: "introduce",
        img: "foods_randname.jpg",
        state: 1,
      },
      picShowNow: "",
      picBlob: "",
      fIDNow: -1,
      UpdateOrAdd: "init",
      HOST: HOST,
      tempUserData: {
        showUserData: false,
        name: "NULL",
        uname: "NULL",
        table_number: "NULL",
      },
    };
  },
  mounted() {
    let myvue = this;
    let lengthOfMsg = -1;
    //定时查询消息,暂定为4秒一次
    setInterval(() => {
      if (myvue.uid != -1) {
        axios({
          method: "get",
          url: "https://" + HOST + "/msg/get?uid=" + myvue.uid,
          headers: {
            Authentication: myvue.cookie_of_uid, //登陆被set的cookie
          },
        })
          .then(function (response) {
            if (response["data"]["errno"] != 0) {
              myvue.$toast.success(response["data"]["errmsg"]);
            } else {
              myvue.msgList = response["data"]["msgs"];
              for (let i = 0; i < myvue.msgList.length; i++) {
                myvue.msgList[i].date =
                  myvue.msgList[i].date.substring(0, 4) +
                  "/" +
                  myvue.msgList[i].date.substring(4, 6) +
                  "/" +
                  myvue.msgList[i].date.substring(6, 8) +
                  " " +
                  myvue.msgList[i].date.substring(8, 10) +
                  ":" +
                  myvue.msgList[i].date.substring(10, 12);
              }
              myvue.msgList.sort((a, b) => {
                return a.date < b.date ? 1 : -1;
              });
            }
            if (lengthOfMsg != -1 && lengthOfMsg != myvue.msgList.length) {
              //播放通知音效
              myvue.MsgAudio.play();
            }
            lengthOfMsg = myvue.msgList.length;
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    }, 4000);
  },
  watch: {
    order_active_page(val) {
      this.getAllOrder();
      if (val == 0) {
        this.orderSet.set1 = "设置待支付";
        this.orderSet.set2 = "设置完成";
      } else if (val == 1) {
        this.orderSet.set1 = "设置无效";
        this.orderSet.set2 = "设置已支付";
      } else if (val == 2) {
        this.orderSet.set1 = "设置无效";
        this.orderSet.set2 = "设置完成";
      } else if (val == 3) {
        this.orderSet.set1 = "设置无效";
        this.orderSet.set2 = "设置待支付";
      }
    },
    typeTab(val) {
      this.foodsTypeList = [];
      let myvue = this;
      for (let i = 0; i < this.foodsList.length; i++) {
        if (this.foodsList[i]["type"] == this.typeList[val]) {
          if (myvue.uname == "BUSINESS") {
            myvue.foodsTypeList.push(myvue.foodsList[i]);
          } else {
            if (myvue.foodsList[i]["state"] == 1) {
              myvue.foodsTypeList.push(myvue.foodsList[i]);
            }
          }
        }
      }
    },

    now(val) {
      if (val == "goods") {
        this.getFoodsList();
      } else if (val == "cart") {
        this.showCart();
      } else if (val == "dialogopt") {
      } else if (val == "mine") {
      }
    },
  },
  methods: {
    getFoodsList() {
      let myvue = this;
      this.load = 1;
      axios({
        method: "get",
        url: "https://" + HOST + "/getfoodslist",
        headers: {
          Authentication: myvue.cookie_of_uid, //登陆被set的cookie
        },
      })
        .then(function (response) {
          if (response["data"]["errno"] != 0) {
            myvue.$toast.success(response["data"]["errmsg"]);
          } else {
            //获取食物列表存入foodsList变量
            myvue.foodsList = response["data"]["foodslist"];

            myvue.typeList = [];
            for (let i = 0; i < myvue.foodsList.length; i++) {
              myvue.typeList.push(myvue.foodsList[i]["type"]);
            }
            myvue.typeList = Array.from(new Set(myvue.typeList));
          }

          myvue.foodsTypeList = [];

          for (let i = 0; i < myvue.foodsList.length; i++) {
            if (myvue.foodsList[i]["type"] == myvue.typeList[myvue.typeTab]) {
              if (myvue.uname == "BUSINESS") {
                myvue.foodsTypeList.push(myvue.foodsList[i]);
              } else {
                if (myvue.foodsList[i]["state"] == 1) {
                  myvue.foodsTypeList.push(myvue.foodsList[i]);
                }
              }
            }
          }

          myvue.load = 0;
        })
        .catch(function (error) {
          console.log(error);
          myvue.load = 0;
        });
    },
    getUserInformation(uid) {
      let myvue = this;
      this.tempUserData.showUserData = true;
      setTimeout(() => {
        this.tempUserData.showUserData = false;
      }, 5000);
      axios({
        method: "get",
        url:
          "https://" +
          HOST +
          "/userdata/get?uid=" +
          myvue.uid +
          "&theuid=" +
          uid,
        headers: {
          Authentication: myvue.cookie_of_uid, //登陆被set的cookie
        },
      })
        .then((response) => {
          if (response["data"]["errno"] != 0) {
            myvue.$toast.success(response["data"]["errmsg"]);
          } else {
            myvue.tempUserData.name = response.data.user.name;
            myvue.tempUserData.uname = response.data.user.uname;
            myvue.tempUserData.table_number = response.data.user.table_number;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    showCart() {
      let myvue = this;
      this.load = 1;
      let URL = "?uid=" + myvue.uid;
      axios({
        method: "get",
        url: "https://" + HOST + "/cart/get" + URL,
        headers: {
          Authentication: myvue.cookie_of_uid, //登陆被set的cookie
        },
      })
        .then(function (response) {
          if (response["data"]["errno"] != 0) {
            myvue.$toast.success(response["data"]["errmsg"]);
          } else {
            //获取购物车列表存入cartList变量
            myvue.cartList = response["data"]["foodslist"];
            myvue.cartPrice = 0.0;

            for (let i = 0; i < myvue.cartList.length; i++) {
              myvue.cartPrice +=
                myvue.cartList[i].new_price * myvue.cartList[i].number;
            }
            myvue.cartPrice = myvue.cartPrice.toFixed(2);
          }
          myvue.load = 0;
        })
        .catch(function (error) {
          console.log(error);
          myvue.load = 0;
        });
    },
    clearCart() {
      let myvue = this;
      this.load = 1;
      axios({
        method: "post",
        url: "https://" + HOST + "/cart/delete",
        data: {
          uid: this.uid,
          food_id: "-2",
        },
        headers: {
          Authentication: myvue.cookie_of_uid, //登陆被set的cookie
        },
      })
        .then(function (response) {
          if (response["data"]["errno"] != 0) {
            myvue.$toast.success(response["data"]["errmsg"]);
          } else {
            myvue.$toast.success("已清空");
          }
          myvue.showCart();
          myvue.load = 0;
        })
        .catch(function (error) {
          console.log(error);
          myvue.load = 0;
        });
    },
    makeOrder() {
      let myvue = this;
      this.load = 1;
      axios({
        method: "post",
        url: "https://" + HOST + "/order/make",
        data: {
          uid: this.uid,
          remark: this.remark,
        },
        headers: {
          Authentication: myvue.cookie_of_uid, //登陆被set的cookie
        },
      })
        .then(function (response) {
          if (response["data"]["errno"] != 0) {
            myvue.$toast.success(response["data"]["errmsg"]);
          } else {
            myvue.$toast.success("订单已创建");
          }
          myvue.showCart();
          myvue.load = 0;
        })
        .catch(function (error) {
          console.log(error);
          myvue.load = 0;
        });
    },
    clickMakeOrder() {
      this.$confirm("确认下单？", "提示").then(({ result }) => {
        if (result) {
          this.makeOrder();
        } else {
          this.$toast.message("已取消");
        }
      });
    },
    toggle(panel) {
      this.panel = panel === this.panel ? "" : panel;
    },
    shift() {},
    voice_clicked() {
      if (this.uid == "-1") {
        //未登录状态不执行语音请求
        this.$alert("请先登陆", "提示", {
          okLabel: "确认",
        });
        return;
      }
      if (this.mic == "mic_none") {
        //开始录音
        this.start_voice();
      } else {
        //手动结束录音
        this.hand_end = true;

        clearInterval(this.timer);
        this.end_voice();
      }
    },
    start_voice() {
      this.StartAudio.play();
      let myvue = this;
      this.hand_end = false;
      this.recorder.onprocess = function (duration) {
        let dataArray = myvue.recorder.getRecordAnalyseData();
        let sum = 0;

        for (let i = 0; i < dataArray.length; i++) {
          sum += dataArray[i];
        }
        let ave = sum / dataArray.length;
        sum = 0;
        for (let i = 0; i < dataArray.length; i++) {
          let unit = (ave - dataArray[i]) * (ave - dataArray[i]);
          sum += unit;
        }
        let variance = parseInt(sum / dataArray.length);

        myvue.voice_arr.push(variance);
      };
      this.recorder.start();
      var speaking = false;
      this.timer = setInterval(() => {
        console.log("定时函数timer执行中");
        if (!speaking) {
          //还未开始说话，查看数组是否有大于30的，如果有，则认为开始说话
          for (let i = 0; i < myvue.voice_arr.length; i++) {
            if (myvue.voice_arr[i] > 30) {
              speaking = true;
              break;
            }
          }
        } else {
          //已经开始说话，查看数组是否有大于20的，如果有则不停止，否则停止
          let has = false;
          for (let i = 0; i < myvue.voice_arr.length; i++) {
            if (myvue.voice_arr[i] > 20) {
              has = true;
              break;
            }
          }
          if (!has) {
            clearInterval(myvue.timer);
            if (myvue.hand_end == false) {
              myvue.end_voice();
            }
          }
        }
        //执行完毕后清理数组
        myvue.voice_arr.length = 0;
      }, 1000);

      this.mic = "mic";
      this.dialog_message_list.length = 0;
      this.dialog_message_list.push("聆听中...");
    },
    end_voice() {
      //结束录音
      //this.recorder.play();
      this.vload = true;
      this.dialog_message_list = [];
      this.mic = "mic_none";
      this.recorder.stop();

      let voices = this.recorder.getWAVBlob();
      let formData = new FormData();
      formData.append("voice", voices);

      let myvue = this;
      //从语音获得文字
      axios({
        method: "post",
        url: "https://" + HOST + "/send/voice",
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data", //值得注意的是，这个地方一定要把请求头更改一下
        },
      })
        .then(function (response) {
          myvue.dialog_message_list.push(response["data"]["message"]);
          myvue.user_text = response["data"]["message"];

          //-----从文字获得回答------------------------------------
          let dataJson = {
            content: myvue.user_text,
            uid: myvue.uid,
          };
          axios({
            method: "post",
            url: "https://" + HOST + "/dialog",
            data: dataJson,
            headers: {
              Authentication: myvue.cookie_of_uid, //登陆被set的cookie
            },
          })
            .then(function (response) {
              if (response["data"]["errno"] == "0") {
                myvue.dialog_message_list.push(
                  response["data"]["action"]["reply"]
                );
                myvue.ReplyAction(
                  response["data"]["action"]["opcode"],
                  response["data"]["action"]["parm"]
                );
                let voiceURL = response["data"]["replyurl"];
                //---------------------------------------------

                axios({
                  method: "get",
                  url: "https://" + HOST + voiceURL,
                })
                  .then(function (response) {
                    var mimeString = "audio/mpeg";

                    var byteString = atob(response["data"]); //base64 解码
                    var arrayBuffer = new ArrayBuffer(byteString.length); //创建缓冲数组
                    var intArray = new Uint8Array(arrayBuffer); //创建视图

                    for (var i = 0; i < byteString.length; i++) {
                      intArray[i] = byteString.charCodeAt(i);
                    }
                    let bl = new Blob([intArray], { type: mimeString });

                    let oAudio = document.createElement("audio");
                    oAudio.src = window.URL.createObjectURL(bl);
                    // 播放音乐

                    oAudio.play();
                    oAudio.addEventListener("ended", () => {
                      //TODO:开启下一轮录音，自动多轮对话,如果手动结束则不开启,开关为auto_listen
                      if (
                        myvue.hand_end == false &&
                        myvue.mic == "mic_none" &&
                        myvue.auto_listen
                      ) {
                        setTimeout(() => {
                          myvue.start_voice();
                        }, 800);
                      }
                    });
                  })
                  .catch(function (error) {
                    console.log(error);
                  });
                //---------------------------------------------
              }
            })
            .catch(function (error) {
              console.log(error);
            });
          //--------------------------------------------
          myvue.vload = false;
        })
        .catch(function (error) {
          console.log(error);
          myvue.vload = false;
        });
    },
    submit() {
      //登陆
      if (this.validateForm.isAgree == false) {
        return;
      }
      let myvue = this;
      this.load = 1;
      axios({
        method: "post",
        url: "https://" + HOST + "/login",
        data: {
          uname: myvue.validateForm.username,
          passwd: myvue.validateForm.password,
        },
      })
        .then(function (response) {
          if (response["data"]["errno"] != 0) {
            myvue.$toast.success(response["data"]["errmsg"]);
          } else {
            myvue.uid = response["data"]["ID"];
            myvue.uname = myvue.validateForm.username;
            myvue.cookie_of_uid =
              response["headers"]["authentication"].split("=")[1];

            myvue.$toast.success("登陆成功!");
            setTimeout(() => {
              myvue.$toast.message(myvue.uname + ",欢迎回来!");
            }, 3000);
            //获取用户信息
            axios({
              method: "get",
              url:
                "https://" +
                HOST +
                "/userdata/get?uid=" +
                myvue.uid +
                "&theuid=" +
                myvue.uid,
              headers: {
                Authentication: myvue.cookie_of_uid, //登陆被set的cookie
              },
            })
              .then((response) => {
                if (response["data"]["errno"] != 0) {
                  myvue.$toast.success(response["data"]["errmsg"]);
                } else {
                  myvue.phone = response.data.user.phone;
                  myvue.table_number = response.data.user.table_number;
                }
              })
              .catch((error) => {
                console.log(error);
              });
            //TODO:根据url填入桌号，url可采用二维码形式，修改桌号请求
            let TB = window.location.search;
            if (TB != "" && TB[0] == "?") {
              TB = TB.substring(1);
            }
            console.log(TB);
            TB = TB.split("&");
            TB = TB[0].split("=");
            if (TB.length == 2 && TB[0] == "table_number") {
              TB = TB[1];
              axios({
                method: "post",
                url: "https://" + HOST + "/userdata/update",
                data: {
                  uid: myvue.uid,
                  updateid: myvue.uid,
                  event: "table_number",
                  parm: TB,
                },
                headers: {
                  Authentication: myvue.cookie_of_uid, //登陆被set的cookie
                },
              })
                .then(function (response) {
                  if (response["data"]["errno"] != 0) {
                    myvue.$toast.success(response["data"]["errmsg"]);
                  } else {
                    myvue.table_number = TB;
                  }
                })
                .catch(function (error) {
                  console.log(error);
                });
            }
          }
          myvue.load = 0;
        })
        .catch(function (error) {
          console.log(error);
          myvue.load = 0;
        });
    },
    logout() {
      this.menu = false;
      this.uid = "-1";
      this.uname = "NULL";
      this.cookie_of_uid = "-1";
      this.$toast.success("退出成功");
    },
    registerNow() {
      let myvue = this;
      if (this.register.passwd != this.register.confirmpwd) {
        myvue.$toast.error("密码不一致");
        return;
      }

      this.load = 1;
      axios({
        method: "post",
        url: "https://" + HOST + "/register",
        data: {
          name: myvue.register.name,
          addresss: myvue.register.addresss,
          phone: myvue.register.phone,
          uname: myvue.register.uname,
          passwd: myvue.register.passwd,
        },
      })
        .then((response) => {
          if (response["data"]["errno"] != 0) {
            myvue.$toast.success(response["data"]["errmsg"]);
          } else {
            myvue.$toast.success("注册成功！请登陆");
            myvue.registerOpen = !myvue.registerOpen;
          }
          myvue.load = 0;
        })
        .catch((error) => {
          console.log(error);
          myvue.load = 0;
        });
    },
    show_aggrement() {
      this.$alert("balabala", "用户协议", {
        okLabel: "确认",
      });
    },
    changes(parm) {
      this.$prompt("请输入：", "修改").then(({ result, value }) => {
        if (result) {
          if (parm == "phone") {
            let myvue = this;
            axios({
              method: "post",
              url: "https://" + HOST + "/userdata/update",
              data: {
                uid: myvue.uid,
                updateid: myvue.uid,
                event: parm,
                parm: value,
              },
              headers: {
                Authentication: myvue.cookie_of_uid, //登陆被set的cookie
              },
            })
              .then(function (response) {
                if (response["data"]["errno"] != 0) {
                  myvue.$toast.success(response["data"]["errmsg"]);
                } else {
                  myvue.$toast.success("修改成功！");
                  myvue.phone = value;
                }
              })
              .catch(function (error) {
                console.log(error);
              });
          } else if (parm == "table_number") {
            let myvue = this;
            axios({
              method: "post",
              url: "https://" + HOST + "/userdata/update",
              data: {
                uid: myvue.uid,
                updateid: myvue.uid,
                event: parm,
                parm: value,
              },
              headers: {
                Authentication: myvue.cookie_of_uid, //登陆被set的cookie
              },
            })
              .then(function (response) {
                if (response["data"]["errno"] != 0) {
                  myvue.$toast.success(response["data"]["errmsg"]);
                } else {
                  myvue.$toast.success("修改成功！");
                  myvue.table_number = value;
                }
              })
              .catch(function (error) {
                console.log(error);
              });
          }
        }
      });
    },
    getQueryVariable(variable) {
      var query = window.location.search.substring(1);
      var vars = query.split("&");
      for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) {
          return pair[1];
        }
      }
      return false;
    },
    showDetail(each) {
      this.describe = each.introduce + "<br/>" + each.new_price + "元即可加购~";
      this.openDetail = true;
      this.fIDNow = each.ID;
    },
    addIntoCart(fID) {
      //这个请求比较快就不显示加载动画了
      let myvue = this;
      axios({
        method: "post",
        url: "https://" + HOST + "/cart/add",
        data: {
          uid: myvue.uid,
          food_id: fID,
        },
        headers: {
          Authentication: myvue.cookie_of_uid, //登陆被set的cookie
        },
      })
        .then(function (response) {
          if (response["data"]["errno"] != 0) {
            myvue.$toast.success(response["data"]["errmsg"]);
          } else {
            myvue.$toast.success("添加成功！");
          }
          myvue.showCart();
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    deleteFromCart(fID) {
      //这个请求比较快就不显示加载动画了
      let myvue = this;
      axios({
        method: "post",
        url: "https://" + HOST + "/cart/delete",
        data: {
          uid: myvue.uid,
          food_id: fID,
        },
        headers: {
          Authentication: myvue.cookie_of_uid, //登陆被set的cookie
        },
      })
        .then(function (response) {
          if (response["data"]["errno"] != 0) {
            myvue.$toast.success(response["data"]["errmsg"]);
          } else {
            myvue.$toast.success("删除成功！");
          }
          myvue.showCart(); //刷新购物车页面
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    showOrder(order) {
      //展示订单详情
      this.orderDetailOpen = true;
      this.theOrder = order;

      let myvue = this;
      this.load = 1;
      axios({
        method: "get",
        url: "https://" + HOST + "/getfoodslist",
        headers: {
          Authentication: myvue.cookie_of_uid, //登陆被set的cookie
        },
      })
        .then(function (response) {
          if (response["data"]["errno"] != 0) {
            myvue.$toast.success(response["data"]["errmsg"]);
          } else {
            //获取食物列表存入foodsList变量
            myvue.foodsList = response["data"]["foodslist"];
            //筛选出在myvue.theOrder的food_id里面的，更换
            let idList = myvue.theOrder.food_id.split(";");
            let fList = [];
            for (let i = 0; i < idList.length; i++) {
              let val = myvue.foodsList.find((val) => {
                return val.ID == idList[i];
              });
              if (val) {
                let index = fList.findIndex((value) => {
                  return value.ID == val.ID;
                });
                if (index != -1) {
                  fList[index].number++;
                } else {
                  fList.push(val);
                  fList[fList.length - 1].number = 1;
                }
              }
            }
            myvue.orderFoodsList = fList;
          }

          myvue.load = 0;
        })
        .catch(function (error) {
          console.log(error);
          myvue.load = 0;
        });
    },
    getAllOrder() {
      let myvue = this;
      this.load = 1;
      if (this.uname != "BUSINESS") {
        let URL = "?uid=" + myvue.uid;
        axios({
          method: "get",
          url: "https://" + HOST + "/order/get/user" + URL,
          headers: {
            Authentication: myvue.cookie_of_uid, //登陆被set的cookie
          },
        })
          .then(function (response) {
            if (response["data"]["errno"] != 0) {
              myvue.$toast.success(response["data"]["errmsg"]);
            } else {
              //获取订单列表存入orderList变量
              myvue.orderList = response["data"]["orders"];
              myvue.orderList.sort((a, b) => {
                return a.date < b.date ? 1 : -1;
              });
              let l = myvue.orderList.length;
              for (let i = 0; i < l; i++) {
                myvue.orderList[i].date =
                  myvue.orderList[i].date.substring(0, 4) +
                  "年" +
                  myvue.orderList[i].date.substring(4, 6) +
                  "月" +
                  myvue.orderList[i].date.substring(6, 8) +
                  "日 " +
                  myvue.orderList[i].date.substring(8, 10) +
                  ":" +
                  myvue.orderList[i].date.substring(10, 12) +
                  ":" +
                  myvue.orderList[i].date.substring(12);
                if (myvue.order_active_page == 0) {
                  continue;
                } else if (myvue.order_active_page == 1) {
                  if (
                    myvue.orderList[i].pay_state != 0 ||
                    myvue.orderList[i].serve_state != 0
                  ) {
                    myvue.orderList.splice(i, 1);
                    i--;
                    l--;
                  }
                } else if (myvue.order_active_page == 2) {
                  if (
                    myvue.orderList[i].pay_state != 1 ||
                    myvue.orderList[i].serve_state != 1
                  ) {
                    myvue.orderList.splice(i, 1);
                    i--;
                    l--;
                  }
                } else if (myvue.order_active_page == 3) {
                  if (
                    myvue.orderList[i].pay_state != 1 ||
                    myvue.orderList[i].serve_state != 2
                  ) {
                    myvue.orderList.splice(i, 1);
                    i--;
                    l--;
                  }
                }
              }
            }
            myvue.load = 0;
          })
          .catch(function (error) {
            console.log(error);
            myvue.load = 0;
          });
      } else {
        console.log("商家获取订单");
        //商家在获取所有用户订单
        let URL = "?uid=" + myvue.uid;
        if (this.order_active_page == 0) {
          //console.log("点击了无效")
          URL += "&state_type=invalid";
        } else if (this.order_active_page == 1) {
          //console.log("点击了待支付")
          URL += "&state_type=unpaid";
        } else if (this.order_active_page == 2) {
          //console.log("点击了待服务")
          URL += "&state_type=paid";
        } else if (this.order_active_page == 3) {
          //console.log("点击了已完成")
          URL += "&state_type=served";
        }
        axios({
          method: "get",
          url: "https://" + HOST + "/order/get/business" + URL,
          headers: {
            Authentication: myvue.cookie_of_uid, //登陆被set的cookie
          },
        })
          .then(function (response) {
            if (response["data"]["errno"] != 0) {
              myvue.$toast.success(response["data"]["errmsg"]);
            } else {
              //获取订单列表存入orderList变量
              myvue.orderList = response["data"]["orders"];
              myvue.orderList.sort((a, b) => {
                return a.date < b.date ? 1 : -1;
              });
              let l = myvue.orderList.length;
              for (let i = 0; i < l; i++) {
                myvue.orderList[i].date =
                  myvue.orderList[i].date.substring(0, 4) +
                  "年" +
                  myvue.orderList[i].date.substring(4, 6) +
                  "月" +
                  myvue.orderList[i].date.substring(6, 8) +
                  "日 " +
                  myvue.orderList[i].date.substring(8, 10) +
                  ":" +
                  myvue.orderList[i].date.substring(10, 12) +
                  ":" +
                  myvue.orderList[i].date.substring(12);
              }
            }
            myvue.load = 0;
          })
          .catch(function (error) {
            console.log(error);
            myvue.load = 0;
          });
      }
    },
    editFood(fID) {
      //弹出详情商品详情页面，编辑各项参数（除了id外），确认后修改,不可删除，但可设置有效位为0
      console.log("编辑商品信息页面");
      //获取foodDetailList

      for (let i = 0; i < this.foodsList.length; i++) {
        if (fID == this.foodsList[i].ID) {
          this.foodDetailList.id = fID;
          this.foodDetailList.name = this.foodsList[i].name;
          this.foodDetailList.type = this.foodsList[i].type;
          this.foodDetailList.old_price = this.foodsList[i].old_price;
          this.foodDetailList.new_price = this.foodsList[i].new_price;
          this.foodDetailList.introduce = this.foodsList[i].introduce;
          this.foodDetailList.img = this.foodsList[i].img;
          this.foodDetailList.state = this.foodsList[i].state;
          break;
        }
      }
      this.picShowNow =
        "https://" + HOST + "/img?imgname=" + this.foodDetailList.img;
    },
    getBase64ByURL(imgUrl) {
      return new Promise((resolve) => {
        window.URL = window.URL || window.webkitURL;
        var xhr = new XMLHttpRequest();
        xhr.open("get", imgUrl, true);
        xhr.responseType = "blob";
        xhr.onload = function () {
          if (this.status == 200) {
            var blob = this.response;
            let oFileReader = new FileReader();
            oFileReader.onloadend = function (e) {
              resolve({ blob, base64: e.target.result });
            };
            oFileReader.readAsDataURL(blob);
          }
        };
        xhr.send();
      });
    },
    updateFoodClicked(foodDetailList) {
      this.foodDetail = !this.foodDetail;
      this.load = 1;
      let myvue = this;
      let formData = new FormData();
      this.getBase64ByURL(this.picShowNow).then((res) => {
        let { blob, base64 } = res;

        myvue.picBlob = blob;

        formData.append("uid", this.uid);
        formData.append("fid", foodDetailList.id);
        formData.append("name", foodDetailList.name);
        formData.append("type", foodDetailList.type);
        formData.append("old_price", foodDetailList.old_price);
        formData.append("new_price", foodDetailList.new_price);
        formData.append("introduce", foodDetailList.introduce);
        formData.append("img", myvue.picBlob);
        formData.append("state", foodDetailList.state);

        if (this.UpdateOrAdd == "update") {
          axios({
            method: "post",
            url: "https://" + HOST + "/foods/update",
            data: formData,
            headers: {
              "Content-Type": "multipart/form-data", //值得注意的是，这个地方一定要把请求头更改一下
              Authentication: myvue.cookie_of_uid, //登陆被set的cookie
            },
          })
            .then(function (response) {
              if (response["data"]["errno"] != 0) {
                myvue.$toast.success(response["data"]["errmsg"]);
              }
              myvue.load = 0;
              //刷新
              myvue.getFoodsList();
            })
            .catch(function (error) {
              console.log(error);
              myvue.load = 0;
            });
        } else if (this.UpdateOrAdd == "add") {
          axios({
            method: "post",
            url: "https://" + HOST + "/foods/add",
            data: formData,
            headers: {
              "Content-Type": "multipart/form-data", //值得注意的是，这个地方一定要把请求头更改一下
              Authentication: myvue.cookie_of_uid, //登陆被set的cookie
            },
          })
            .then(function (response) {
              if (response["data"]["errno"] != 0) {
                myvue.$toast.success(response["data"]["errmsg"]);
              }
              myvue.load = 0;
              myvue.getFoodsList();
            })
            .catch(function (error) {
              console.log(error);
              myvue.load = 0;
            });
        }
      });
    },
    showPicChoosed() {
      let file = document.getElementById("img").files[0];
      if (!/image\/\w+/.test(file.type)) {
        this.$message.error("文件必须为图片！");
      }
      var imageURL = window.URL.createObjectURL(
        new Blob([file], { type: "image/jpeg" })
      );
      this.picShowNow = imageURL;
    },
    addFood() {
      //添加新食物，同样弹出那个详情框（id为空），确认后添加

      this.foodDetailList.id = -1;
      this.foodDetailList.name = "";
      this.foodDetailList.type = "";
      this.foodDetailList.old_price = "";
      this.foodDetailList.new_price = "";
      this.foodDetailList.introduce = "";
      this.foodDetailList.img = "";
      this.foodDetailList.state = 1;

      this.picShowNow =
        "https://" + HOST + "/img?imgname=" + this.foodDetailList.img;
    },
    changePwd() {
      //弹窗修改密码，点击确认发送请求
    },
    alreadyRead(ID) {
      let myvue = this;
      axios({
        method: "post",
        url: "https://" + HOST + "/msg/read",
        data: {
          msg_id: ID,
          uid: myvue.uid,
        },
        headers: {
          Authentication: myvue.cookie_of_uid, //登陆被set的cookie
        },
      })
        .then(function (response) {
          if (response["data"]["errno"] != 0) {
            myvue.$toast.success(response["data"]["errmsg"]);
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    orderSet_1Clicked() {
      let OID = this.theOrder.ID;
      let myvue = this;
      this.load = 1;
      if (this.orderSet.set1 == "设置待支付") {
        axios({
          method: "post",
          url: "https://" + HOST + "/order/update",
          data: {
            uid: myvue.uid,
            oid: OID,
            event: "unpaid",
          },
          headers: {
            Authentication: myvue.cookie_of_uid, //登陆被set的cookie
          },
        })
          .then(function (response) {
            if (response["data"]["errno"] != 0) {
              myvue.$toast.success(response["data"]["errmsg"]);
            } else {
              myvue.$toast.success("流转成功！");
            }
            myvue.getAllOrder();
            myvue.load = 0;
            myvue.orderDetailOpen = !myvue.orderDetailOpen;
          })
          .catch(function (error) {
            console.log(error);
            myvue.load = 0;
          });
      } else if (this.orderSet.set1 == "设置无效") {
        axios({
          method: "post",
          url: "https://" + HOST + "/order/update",
          data: {
            uid: myvue.uid,
            oid: OID,
            event: "invalid",
          },
          headers: {
            Authentication: myvue.cookie_of_uid, //登陆被set的cookie
          },
        })
          .then(function (response) {
            if (response["data"]["errno"] != 0) {
              myvue.$toast.success(response["data"]["errmsg"]);
            } else {
              myvue.$toast.success("流转成功！");
            }
            myvue.getAllOrder();
            myvue.load = 0;
            myvue.orderDetailOpen = !myvue.orderDetailOpen;
          })
          .catch(function (error) {
            console.log(error);
            myvue.load = 0;
          });
      }
    },
    orderSet_2Clicked() {
      let OID = this.theOrder.ID;
      let myvue = this;
      this.load = 1;
      if (this.orderSet.set2 == "设置待支付") {
        axios({
          method: "post",
          url: "https://" + HOST + "/order/update",
          data: {
            uid: myvue.uid,
            oid: OID,
            event: "unpaid",
          },
          headers: {
            Authentication: myvue.cookie_of_uid, //登陆被set的cookie
          },
        })
          .then(function (response) {
            if (response["data"]["errno"] != 0) {
              myvue.$toast.success(response["data"]["errmsg"]);
            } else {
              myvue.$toast.success("流转成功！");
            }
            myvue.getAllOrder();
            myvue.load = 0;
            myvue.orderDetailOpen = !myvue.orderDetailOpen;
          })
          .catch(function (error) {
            console.log(error);
            myvue.load = 0;
          });
      } else if (this.orderSet.set2 == "设置完成") {
        axios({
          method: "post",
          url: "https://" + HOST + "/order/update",
          data: {
            uid: myvue.uid,
            oid: OID,
            event: "served",
          },
          headers: {
            Authentication: myvue.cookie_of_uid, //登陆被set的cookie
          },
        })
          .then(function (response) {
            if (response["data"]["errno"] != 0) {
              myvue.$toast.success(response["data"]["errmsg"]);
            } else {
              myvue.$toast.success("流转成功！");
            }
            myvue.getAllOrder();
            myvue.load = 0;
            myvue.orderDetailOpen = !myvue.orderDetailOpen;
          })
          .catch(function (error) {
            console.log(error);
            myvue.load = 0;
          });
      } else if (this.orderSet.set2 == "设置已支付") {
        axios({
          method: "post",
          url: "https://" + HOST + "/order/update",
          data: {
            uid: myvue.uid,
            oid: OID,
            event: "paid",
          },
          headers: {
            Authentication: myvue.cookie_of_uid, //登陆被set的cookie
          },
        })
          .then(function (response) {
            if (response["data"]["errno"] != 0) {
              myvue.$toast.success(response["data"]["errmsg"]);
            } else {
              myvue.$toast.success("流转成功！");
            }
            myvue.getAllOrder();
            myvue.load = 0;
            myvue.orderDetailOpen = !myvue.orderDetailOpen;
          })
          .catch(function (error) {
            console.log(error);
            myvue.load = 0;
          });
      }
    },
    ReplyAction(opcode, parm) {
      console.log("操作:", opcode, parm);
      if (opcode == "foods") {
        this.now = "goods";
        for (let i = 0; i < this.typeList.length; i++) {
          if (this.typeList[i] == parm) {
            this.typeTab = i;
          }
        }
      } else if (opcode == "addcart") {
        this.addIntoCart(parm);
      } else if (opcode == "deletecart") {
        this.deleteFromCart(parm);
      } else if (opcode == "makeorder") {
        this.makeOrder();
        setTimeout(() => {
          this.now = "mine";
          this.panel = "order";
          this.order_active_page = 1;
        }, 2000);
      } else if (opcode == "logout") {
        this.logout();
      } else if (opcode == "exit") {
        this.auto_listen = false;
      } else if (opcode == "showcart") {
        this.now = "cart";
      } else if (opcode == "clearcart") {
        this.clearCart();
      } else if (opcode == "opencontinue") {
        this.auto_listen = true;
      } else if (opcode == "closecontinue") {
        this.auto_listen = false;
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.demo-container {
  .row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .grid-cell {
    border-radius: 4px;
    height: 36px;
    background: rgba(255, 255, 255, 0.8);
  }
}
.demo-container.is-stripe .col:nth-child(2n) .grid-cell {
  background: rgba(0, 0, 0, 0.54);
}
.mu-ripple-demo {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 16px;
  background-color: #fff;
  border-radius: 4px;
  &.demo-1 {
    color: #cce0f1;
    border: 1px solid #2196f3;
  }
}
.buttom {
  width: 100%;
  position: absolute;
  bottom: 0;
}
.voice {
  width: 88%;
  position: fixed;
  bottom: 10%;
}
.text_area {
  font-size: 18px;
  font-family: Sans-serif;
  text-align: left;
  margin-top: 4%;

  margin-left: 100px;
}
.loading {
  position: absolute;
}
#aggrement:hover {
  color: red;
  cursor: pointer;
}
.mine {
  color: #2196f3;
  position: absolute;
  height: 80%;
  width: 100%;
}
.mine-login {
  font-size: 18px;
  height: 100%;
}
.editicon:hover {
  color: red;
}
.foodspage {
  overflow-y: auto;
  position: absolute;
  top: 15%;
  left: 1%;
  width: 98%;
  height: 78%;
}
.buttons:active {
  color: red;
}
</style>
