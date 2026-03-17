// pages/index/index.js
const app = getApp();
const { authApi, evaluationApi } = require('../../api/api.js');

Page({
  data: {
    hasLogin: false,
    userInfo: null,
    stats: {
      evalCount: 0,
      reportCount: 0,
      remaining: 3
    },
    recentReports: [],
    username: '',
    password: ''
  },
  
  onShow() {
    this.checkLoginStatus();
  },
  
  checkLoginStatus() {
    const token = app.getToken();
    const userInfo = app.getUserInfo();
    
    if (token && userInfo) {
      this.setData({
        hasLogin: true,
        userInfo: userInfo
      });
      this.loadUserData();
    } else {
      this.setData({
        hasLogin: false,
        userInfo: null
      });
    }
  },
  
  inputUsername(e) {
    this.setData({ username: e.detail.value });
  },
  
  inputPassword(e) {
    this.setData({ password: e.detail.value });
  },
  
  async handleLogin() {
    const { username, password } = this.data;
    
    if (!username || !password) {
      wx.showToast({ title: '请输入用户名和密码', icon: 'none' });
      return;
    }
    
    wx.showLoading({ title: '登录中...' });
    
    try {
      const loginResult = await authApi.login(username, password);
      
      if (loginResult.access_token) {
        const userResult = await authApi.getUserInfo();
        
        if (userResult.status === 'success') {
          const userData = userResult.data;
          app.setUserInfo(userData, loginResult.access_token);
          
          this.setData({
            hasLogin: true,
            userInfo: userData
          });
          
          wx.showToast({ title: '登录成功', icon: 'success' });
          this.loadUserData();
        }
      }
    } catch (err) {
      wx.showToast({ title: err.message || '登录失败', icon: 'none' });
    } finally {
      wx.hideLoading();
    }
  },
  
  async loadUserData() {
    const userInfo = this.data.userInfo;
    if (!userInfo) return;
    
    try {
      const vipStatus = await evaluationApi.getVipStatus();
      
      this.setData({
        stats: {
          evalCount: vipStatus.total_evaluations || 0,
          reportCount: vipStatus.total_reports || 0,
          remaining: vipStatus.remaining || 0
        }
      });
      
      const history = await evaluationApi.getHistory(userInfo.id, 5);
      if (history && history.length > 0) {
        this.setData({
          recentReports: history.slice(0, 5)
        });
      }
    } catch (err) {
      console.error('加载用户数据失败', err);
    }
  },
  
  startEvaluate() {
    wx.switchTab({ url: '/pages/form/form' });
  },
  
  viewReport(e) {
    const reportId = e.currentTarget.dataset.id;
    wx.navigateTo({ url: `/pages/report/report?id=${reportId}` });
  }
});
