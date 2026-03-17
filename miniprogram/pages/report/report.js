// pages/report/report.js
const app = getApp();
const { evaluationApi } = require('../../api/api.js');

Page({
  data: {
    reportId: null,
    report: {
      org_name: '',
      total_score: 0,
      maturity_level: '',
      dimensions: [],
      p0_issues: [],
      p1_issues: [],
      suggestions: []
    },
    loading: true
  },
  
  onLoad(options) {
    if (options.id) {
      this.setData({ reportId: options.id });
      this.loadReport(options.id);
    }
  },
  
  async loadReport(reportId) {
    wx.showLoading({ title: '加载中...' });
    
    try {
      const result = await evaluationApi.getResult(reportId);
      
      if (result.status === 'success') {
        const data = result.data;
        
        const report = {
          org_name: data.org_name || '',
          total_score: data.total_score || 0,
          maturity_level: data.maturity_level || '',
          risk_level: data.risk_level || '',
          dimensions: data.detail_json?.dimensions || [],
          p0_issues: data.detail_json?.p0_issues || [],
          p1_issues: data.detail_json?.p1_issues || [],
          suggestions: data.detail_json?.suggestions || []
        };
        
        this.setData({ report });
      }
    } catch (err) {
      wx.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
      wx.hideLoading();
    }
  },
  
  viewFullReport() {
    wx.navigateTo({
      url: `/pages/report/detail?id=${this.data.reportId}`
    });
  },
  
  shareReport() {
    wx.showShareMenu({
      withShareTicket: true
    });
  }
});
