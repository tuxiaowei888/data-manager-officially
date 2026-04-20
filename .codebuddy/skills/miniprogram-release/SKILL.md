---
name: "miniprogram-release"
description: "微信小程序发布准备和审核指南。适用于发布检查、版本管理、提交审核。当用户要求发布小程序或准备提交审核时调用。"
---

# 微信小程序发布准备

## 概述

小程序发布需要经过多个检查步骤，确保代码质量和合规性。本指南覆盖发布前的检查清单和提交流程。

## 发布前检查清单

### 1. 功能检查

- [ ] 所有页面正常访问，无死链
- [ ] 表单提交功能正常
- [ ] API 请求全部返回正确数据
- [ ] 登录/登出流程正常
- [ ] 错误提示友好且正确
- [ ] Loading 状态显示正常

### 2. 界面检查

- [ ] 适配不同屏幕尺寸（iPhone SE ~ iPhone 15 Pro Max）
- [ ] 文字无截断、溢出
- [ ] 图片正常加载
- [ ] 导航 TabBar 正常切换
- [ ] 无样式错乱问题

### 3. 权限检查

- [ ] 已申请必要的用户权限（位置、相机等）
- [ ] 隐私政策弹窗（如需要）
- [ ] 用户协议页面（如需要）

### 4. 配置检查

```json
// project.config.json
{
  "appid": "your_appid",
  "projectname": "shuwei-data-manager",
  "setting": {
    "urlCheck": false,
    "es6": true,
    "enhance": true,
    "postcss": true,
    "preloadBackgroundData": false,
    "minified": true,
    "newFeature": true,
    "coverView": true,
    "nodeModules": false,
    "autoAudits": false,
    "showShadowRootInWxmlPanel": true,
    "scopeDataCheck": false,
    "uglifyFileName": false,
    "checkInvalidKey": true,
    "checkSiteMap": true,
    "uploadWithSourceMap": true,
    "compileHotReLoad": false,
    "useMultiFrameRuntime": true,
    "useApiHook": true,
    "useApiHostProcess": true,
    "babelSetting": {
      "ignore": [],
      "disablePlugins": [],
      "outputPath": ""
    },
    "useIsolateContext": true,
    "userConfirmedBundleSwitch": false,
    "packNpmManually": false,
    "packNpmRelationList": [],
    "minifyWXSS": true
  }
}
```

### 5. 版本号管理

```javascript
// app.json
{
  "version": "1.0.0",     // 小程序版本号
  "versionDesc": "优化页面加载速度"  // 版本说明
}
```

版本号规则：
- 主版本号.次版本号.修订号
- 主版本号：不兼容的重大更新
- 次版本号：向下兼容的功能新增
- 修订号：向下兼容的问题修复

## 代码上传

### 1. 开发者工具操作

1. 打开微信开发者工具
2. 登录并选择项目
3. 点击「上传」按钮
4. 填写版本号和备注
5. 确认上传

### 2. 命令行上传（如需要）

```bash
# 安装 miniprogram-ci
npm install -g miniprogram-ci

# 上传
miniprogram-ci upload \
  --appid your_appid \
  --privateKeyPath ./private.your_appid.key \
  --project ./dist \
  --version 1.0.0 \
  --desc '版本描述'
```

## 登录微信公众平台

### 1. 版本管理

1. 访问 https://mp.weixin.qq.com
2. 进入「版本管理」
3. 查看已上传的版本
4. 选择「提交审核」或「体验版」

### 2. 体验版测试

- 生成体验版二维码
- 分享给测试人员
- 测试所有核心流程
- 检查是否有权限提示

## 提交审核

### 1. 审核信息填写

- 版本号：自动填充
- 版本描述：简要说明功能
- 功能页面：选择需要审核的页面
- 测试账号（如需要）：提供测试账号密码

### 2. 审核类目

根据小程序实际内容选择正确的类目：
- 工具 → 信息查询
- 商业服务 → 企业服务
- 等等

### 3. 常见审核被拒原因

| 原因 | 解决方案 |
|:---|:---|
| 没有清晰的反馈机制 | 添加客服联系方式或问题反馈入口 |
| 隐私政策不完善 | 添加隐私政策页面和用户同意弹窗 |
| 诱导分享 | 移除任何诱导分享文案 |
| 虚拟支付 | 移除虚拟商品购买功能 |
| 资质不全 | 根据类目补充相关资质证明 |

## 审核时效

- 普通审核：7 个工作日内
- 加急审核：3 个工作日内（需要付费）
- 驳回后重新提交：从头计算时间

## 发布后检查

- [ ] 确认已发布版本正确
- [ ] 检查版本号是否更新
- [ ] 确认所有功能正常
- [ ] 监控错误日志

## 常见问题

### 1. 如何回滚版本？

在微信公众平台「版本管理」中，可以选择任意历史版本「设为体验版」或直接发布。

### 2. 如何查看用户反馈？

在微信公众平台「用户反馈」中查看用户提交的问题和建议。

### 3. 小程序码不生效？

检查 appid 是否正确，域名是否已加入白名单。

## 适用场景

- 小程序首次发布
- 版本更新提交审核
- 体验版测试
- 审核被拒后修改
