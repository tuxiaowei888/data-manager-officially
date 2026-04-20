---
name: "miniprogram-state"
description: "微信小程序状态管理和数据流指南。适用于 globalData、页面间通信、数据缓存、状态持久化。当用户要求管理小程序状态时调用。"
---

# 微信小程序状态管理

## 概述

小程序的状态管理涉及全局状态（globalData）、页面间通信、数据缓存。本指南覆盖常见的状态管理场景和最佳实践。

## globalData 管理

### App.js 中的全局状态

```javascript
// app.js
App({
  globalData: {
    userInfo: null,
    token: null,
    baseUrl: 'http://localhost:8000/api/v1',
    vipStatus: null,
    config: {}
  },

  onLaunch() {
    // 初始化时从缓存恢复
    const token = wx.getStorageSync('token');
    const userInfo = wx.getStorageSync('userInfo');

    if (token) {
      this.globalData.token = token;
      this.globalData.userInfo = userInfo;
    }
  },

  // 统一的状态访问方法
  getUserInfo() {
    return this.globalData.userInfo;
  },

  getToken() {
    return this.globalData.token;
  },

  setUserInfo(userInfo, token) {
    this.globalData.userInfo = userInfo;
    this.globalData.token = token;
    // 持久化到缓存
    wx.setStorageSync('userInfo', userInfo);
    wx.setStorageSync('token', token);
  },

  clearUserInfo() {
    this.globalData.userInfo = null;
    this.globalData.token = null;
    wx.removeStorageSync('userInfo');
    wx.removeStorageSync('token');
  },

  isLoggedIn() {
    return !!this.globalData.token;
  }
});
```

## 页面间通信

### 1. URL 参数传递

```javascript
// 跳转时传递
wx.navigateTo({
  url: '/pages/report/report?id=123&type=summary'
});

// 接收时获取
onLoad(options) {
  console.log(options.id);    // 123
  console.log(options.type); // summary
}
```

### 2. 事件通信

```javascript
// 页面 A - 触发事件
wx.navigateTo({
  url: '/pages/form/form',
  events: {
    // 事件处理函数
    onFormSubmit: (data) => {
      console.log('收到表单数据', data);
    }
  }
});

// 页面 B - 触发事件并返回
const eventChannel = this.getOpenerEventChannel();
eventChannel.emit('onFormSubmit', { result: 'success' });
wx.navigateBack();
```

### 3. EventChannel

```javascript
// 页面 A
onLoad() {
  wx.navigateTo({
    url: '/pages/detail/detail',
    success: (res) => {
      res.eventChannel.emit('acceptData', { data: 'fromPageA' });
    }
  });
}

// 页面 B
onLoad() {
  const eventChannel = this.getOpenerEventChannel();
  eventChannel.on('acceptData', (data) => {
    console.log(data); // { data: 'fromPageA' }
  });
}
```

## 数据缓存

### 同步缓存 API

```javascript
// 存储
wx.setStorageSync('key', 'value');
wx.setStorageSync('user', { name: '张三', age: 18 });

// 读取
const value = wx.getStorageSync('key');
const user = wx.getStorageSync('user');

// 删除
wx.removeStorageSync('key');

// 清空
wx.clearStorageSync();
```

### 异步缓存 API

```javascript
// 存储
wx.setStorage({
  key: 'user',
  data: { name: '张三' },
  success: () => console.log('存储成功')
});

// 读取
wx.getStorage({
  key: 'user',
  success: (res) => console.log(res.data)
});

// 获取所有 key
wx.getStorageInfo({
  success: (res) => {
    console.log(res.keys);     // 所有 key
    console.log(res.currentSize); // 当前大小 KB
    console.log(res.limitSize);  // 限制大小 KB
  }
});
```

### 缓存大小限制

- 单个 key 不超过 1MB
- 总缓存不超过 10MB
- 超过限制自动清除最早访问的数据

## 页面状态管理

### 页面状态恢复

```javascript
// 页面 A - 进入前保存状态
onUnload() {
  const state = this.data;
  wx.setStorageSync('pageAState', state);
},

// 页面 A - 恢复状态
onLoad() {
  const savedState = wx.getStorageSync('pageAState');
  if (savedState) {
    this.setData(savedState);
    wx.removeStorageSync('pageAState');
  }
}
```

### 登录状态检查

```javascript
// app.js
checkLogin() {
  if (!this.globalData.token) {
    wx.redirectTo({ url: '/pages/index/index' });
    return false;
  }
  return true;
},

// 页面中使用
onLoad() {
  if (!app.checkLogin()) {
    return;
  }
  // 加载页面数据...
}
```

## 状态管理模式

### 简单 Store 模式

```javascript
// store/userStore.js
const userStore = {
  state: {
    userInfo: null,
    token: null,
    isVip: false
  },

  setUser(userInfo, token) {
    this.state.userInfo = userInfo;
    this.state.token = token;
    this.state.isVip = userInfo?.user_type === 'vip';
    wx.setStorageSync('user', this.state);
  },

  clearUser() {
    this.state = {
      userInfo: null,
      token: null,
      isVip: false
    };
    wx.removeStorageSync('user');
  },

  init() {
    const saved = wx.getStorageSync('user');
    if (saved) {
      this.state = { ...this.state, ...saved };
    }
  }
};

module.exports = userStore;
```

## 最佳实践

1. **globalData 集中管理**：所有全局状态通过 App 实例访问
2. **缓存持久化**：关键数据（token、用户信息）需要持久化
3. **状态恢复**：页面切换时保存和恢复状态
4. **登录拦截**：需要登录的页面统一检查登录态
5. **避免存储大文件**：缓存有限，合理使用

## 适用场景

- 用户登录状态管理
- 页面间数据传递
- 表单数据暂存
- 用户偏好设置
- 离线数据缓存
