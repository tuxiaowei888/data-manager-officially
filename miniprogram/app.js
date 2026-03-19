/**
 * 数维数据管家小程序 - 入口文件
 */

App({
  globalData: {
    userInfo: null,
    token: null,
    baseUrl: 'http://localhost:8000/api/v1'
  },
  
  onLaunch() {
    const token = wx.getStorageSync('token');
    const userInfo = wx.getStorageSync('userInfo');
    
    if (token) {
      this.globalData.token = token;
      this.globalData.userInfo = userInfo;
    }
  },
  
  getUserInfo() {
    return this.globalData.userInfo;
  },
  
  getToken() {
    return this.globalData.token;
  },
  
  setUserInfo(userInfo, token) {
    this.globalData.userInfo = userInfo;
    this.globalData.token = token;
    wx.setStorageSync('userInfo', userInfo);
    wx.setStorageSync('token', token);
  },
  
  clearUserInfo() {
    this.globalData.userInfo = null;
    this.globalData.token = null;
    wx.removeStorageSync('userInfo');
    wx.removeStorageSync('token');
  },
  
  checkLogin() {
    if (!this.globalData.token) {
      wx.redirectTo({
        url: '/pages/index/index'
      });
      return false;
    }
    return true;
  }
});
