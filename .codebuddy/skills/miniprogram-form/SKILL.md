---
name: "miniprogram-form"
description: "微信小程序表单处理和验证指南。适用于表单验证、数据绑定、多步表单、表单提交。当用户要求开发小程序表单功能时调用。"
---

# 微信小程序表单处理

## 概述

小程序表单涉及数据绑定、用户输入验证、多步表单状态管理。本指南针对数维数据管家项目的评估表单场景。

## 项目表单结构

```
miniprogram/pages/form/
├── form.js      # 表单逻辑
├── form.json     # 页面配置
├── form.wxml     # 表单模板
└── form.wxss     # 表单样式
```

## 数据绑定

### Page data 结构设计

```javascript
Page({
  data: {
    currentStep: 1,           // 当前步骤
    totalSteps: 6,            // 总步骤数
    submitting: false,        // 提交状态

    formData: {
      // 第一步：企业信息
      org_name: '',
      org_code: '',
      industry: '',
      company_size: '',

      // 第二步：数据情况
      data_types: [],
      data_volume: '',
      update_frequency: '',

      // 第三步：合规情况
      compliance_source: 'yes',
      compliance_privacy: 'yes',
      compliance_auth: 'yes',

      // 第四步：数据质量
      quality_completeness: 50,
      quality_accuracy: 50,
      quality_timeliness: 50,

      // 第五步：应用场景
      scenario_count: '',
      annual_revenue: '',
      cost_saving: '',

      // 第六步：确认提交
    }
  }
});
```

## 输入绑定

### 文本输入

```xml
<input
  value="{{formData.org_name}}"
  bindinput="onOrgNameInput"
  placeholder="请输入企业名称"
/>
```

```javascript
onOrgNameInput(e) {
  this.setData({
    'formData.org_name': e.detail.value
  });
}
```

### 选择器绑定

```xml
<picker
  mode="selector"
  range="{{industries}}"
  bindchange="onIndustryChange"
>
  <view>{{formData.industry || '请选择行业'}}</view>
</picker>
```

```javascript
onIndustryChange(e) {
  const index = e.detail.value;
  this.setData({
    'formData.industry': this.data.industries[index]
  });
}
```

### 复选框绑定

```xml
<checkbox-group bindchange="onDataTypesChange">
  <checkbox value="user_data" />用户数据
  <checkbox value="transaction_data" />交易数据
  <checkbox value="operation_data" />运营数据
</checkbox-group>
```

```javascript
onDataTypesChange(e) {
  this.setData({
    'formData.data_types': e.detail.value
  });
}
```

### 滑块绑定

```xml
<slider
  min="0"
  max="100"
  value="{{formData.quality_completeness}}"
  bindchange="onQualityChange"
  show-value
/>
```

```javascript
onQualityChange(e) {
  this.setData({
    'formData.quality_completeness': e.detail.value
  });
}
```

## 表单验证

### 验证规则定义

```javascript
const validateRules = {
  org_name: {
    required: true,
    message: '请输入企业名称'
  },
  industry: {
    required: true,
    message: '请选择行业'
  },
  data_types: {
    required: true,
    validator: (value) => value.length > 0,
    message: '请至少选择一项数据类型'
  }
};
```

### 验证函数

```javascript
validateForm() {
  const { formData } = this.data;

  // 第一步必填验证
  if (!formData.org_name) {
    wx.showToast({ title: '请输入企业名称', icon: 'none' });
    return false;
  }

  if (!formData.industry) {
    wx.showToast({ title: '请选择行业', icon: 'none' });
    return false;
  }

  if (!formData.data_types || formData.data_types.length === 0) {
    wx.showToast({ title: '请选择数据类型', icon: 'none' });
    return false;
  }

  return true;
}
```

## 多步表单

### 步骤导航

```javascript
nextStep() {
  // 验证当前步骤
  if (!this.validateCurrentStep()) {
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

validateCurrentStep() {
  const { currentStep, formData } = this.data;

  switch (currentStep) {
    case 1:
      if (!formData.org_name) {
        wx.showToast({ title: '请输入企业名称', icon: 'none' });
        return false;
      }
      break;
    // 其他步骤验证...
  }
  return true;
}
```

### 步骤指示器

```xml
<view class="step-indicator">
  <view
    wx:for="{{totalSteps}}"
    wx:key="index"
    class="step {{index + 1 <= currentStep ? 'active' : ''}}"
  >
    {{index + 1}}
  </view>
</view>
```

## 表单提交

### 提交处理

```javascript
async submitForm() {
  // 最终验证
  if (!this.validateForm()) {
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
      wx.showToast({
        title: result.message || '评估失败',
        icon: 'none'
      });
    }
  } catch (err) {
    wx.showToast({
      title: err.detail || err.message || '评估失败',
      icon: 'none'
    });
  } finally {
    this.setData({ submitting: false });
    wx.hideLoading();
  }
}
```

## 最佳实践

1. **使用 setData 的路径语法**：如 `'formData.org_name'` 进行部分更新
2. **表单状态集中管理**：所有表单数据放在 formData 对象中
3. **必填字段前端验证**：减少无效请求
4. **提交状态锁定**：防止重复提交
5. **错误提示友好**：使用 `icon: 'none'` 显示文字提示

## 适用场景

- 开发新的表单页面
- 添加表单字段验证
- 实现多步表单向导
- 表单数据提交处理
