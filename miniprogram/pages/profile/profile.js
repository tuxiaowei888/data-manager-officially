// pages/profile/profile.js
const app = getApp();
const { evaluationApi, authApi } = require('../../api/api.js');

Page({
  data: {
    userInfo: null,
    vipStatus: {
      remaining: 0,
      total_evaluations: 0,
      total_reports: 0
    }
  },
  
  onShow() {
    const userInfo = app.getUserInfo();
    if (userInfo) {
      this.setData({ userInfo });
      this.loadVipStatus();
    } else {
      wx.redirectTo({ url: '/pages/index/index' });
    }
  },
  
  async loadVipStatus() {
    try {
      const result = await evaluationApi.getVipStatus();
      this.setData({ vipStatus: result });
    } catch (err) {
      console.error('加载VIP状态失败', err);
    }
  },
  
  viewHistory() {
    wx.navigateTo({ url: '/pages/history/history' });
  },
  
  viewReports() {
    wx.navigateTo({ url: '/pages/report-list/report-list' });
  },
  
  goToWeb() {
    wx.showModal({
      title: '提示',
      content: '请在电脑浏览器访问 http://localhost:8000 使用完整功能',
      showCancel: false
    });
  },
  
  contactService() {
    wx.showModal({
      title: '联系客服',
      content: '咨询热线：13982274410',
      showCancel: false
    });
  },
  
  handleLogout() {
    wx.showModal({
      title: '确认退出',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          app.clearUserInfo();
          wx.redirectTo({ url: '/pages/index/index' });
        }
      }
    });
  }
});
