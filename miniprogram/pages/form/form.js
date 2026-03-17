// pages/form/form.js
const app = getApp();
const { evaluationApi } = require('../../api/api.js');

Page({
  data: {
    currentStep: 1,
    totalSteps: 6,
    submitting: false,
    
    formData: {
      org_name: '',
      org_code: '',
      industry: '',
      company_size: '',
      data_types: [],
      data_volume: '',
      update_frequency: '',
      compliance_source: 'yes',
      compliance_privacy: 'yes',
      compliance_auth: 'yes',
      quality_completeness: 50,
      quality_accuracy: 50,
      quality_timeliness: 50,
      scenario_count: '',
      annual_revenue: '',
      cost_saving: ''
    },
    
    industries: ['互联网', '金融', '制造业', '医疗', '教育', '零售', '物流', '其他'],
    companySizes: ['小型', '中型', '大型', '上市公司'],
    dataTypes: [
      { value: 'user_data', label: '用户数据' },
      { value: 'transaction_data', label: '交易数据' },
      { value: 'operation_data', label: '运营数据' },
      { value: 'sensor_data', label: '传感器数据' },
      { value: 'public_data', label: '公开数据' }
    ],
    yesNoOptions: [
      { value: 'yes', label: '是' },
      { value: 'no', label: '否' }
    ]
  },
  
  onLoad() {
    if (!app.checkLogin()) {
      return;
    }
  },
  
  bindIndustryChange(e) {
    const index = e.detail.value;
    this.setData({
      'formData.industry': this.data.industries[index]
    });
  },
  
  bindSizeChange(e) {
    const index = e.detail.value;
    this.setData({
      'formData.company_size': this.data.companySizes[index]
    });
  },
  
  bindDataTypesChange(e) {
    this.setData({
      'formData.data_types': e.detail.value
    });
  },
  
  bindUpdateTimeChange(e) {
    this.setData({
      'formData.update_frequency': e.detail.value
    });
  },
  
  bindCompliance1Change(e) {
    this.setData({ 'formData.compliance_source': e.detail.value });
  },
  
  bindCompliance2Change(e) {
    this.setData({ 'formData.compliance_privacy': e.detail.value });
  },
  
  bindCompliance3Change(e) {
    this.setData({ 'formData.compliance_auth': e.detail.value });
  },
  
  bindQuality1Change(e) {
    this.setData({ 'formData.quality_completeness': e.detail.value });
  },
  
  bindQuality2Change(e) {
    this.setData({ 'formData.quality_accuracy': e.detail.value });
  },
  
  bindQuality3Change(e) {
    this.setData({ 'formData.quality_timeliness': e.detail.value });
  },
  
  nextStep() {
    if (this.data.currentStep === 1 && !this.data.formData.org_name) {
      wx.showToast({ title: '请输入企业名称', icon: 'none' });
      return;
    }
    
    if (this.data.currentStep < this.data.totalSteps) {
      this.setData({
        currentStep: this.data.currentStep + 1
      });
    }
  },
  
  prevStep() {
    if (this.data.currentStep > 1) {
      this.setData({
        currentStep: this.data.currentStep - 1
      });
    }
  },
  
  async submitForm() {
    if (!this.data.formData.org_name) {
      wx.showToast({ title: '请输入企业名称', icon: 'none' });
      return;
    }
    
    this.setData({ submitting: true });
    wx.showLoading({ title: '评估中...' });
    
    try {
      const result = await evaluationApi.evaluate(this.data.formData);
      
      if (result.status === 'success') {
        wx.showToast({ title: '评估完成', icon: 'success' });
        
        setTimeout(() => {
          wx.navigateTo({
            url: `/pages/report/report?id=${result.data.result_id}`
          });
        }, 1500);
      } else {
        wx.showToast({ title: result.message || '评估失败', icon: 'none' });
      }
    } catch (err) {
      wx.showToast({ title: err.detail || err.message || '评估失败', icon: 'none' });
    } finally {
      this.setData({ submitting: false });
      wx.hideLoading();
    }
  }
});
