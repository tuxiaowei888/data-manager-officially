---
name: "miniprogram-component"
description: "微信小程序自定义组件开发指南。适用于创建组件、组件通信、插槽使用。当用户要求开发小程序组件时调用。"
---

# 微信小程序组件开发

## 概述

微信小程序组件是封装可复用的 UI 和逻辑的基本单元。合理使用组件可以提高代码复用性和可维护性。

## 组件创建流程

### 1. 创建组件目录结构

```
miniprogram/components/
└── my-component/
    ├── my-component.js       # 组件逻辑
    ├── my-component.json     # 组件配置
    ├── my-component.wxml     # 组件模板
    └── my-component.wxss     # 组件样式
```

### 2. 组件配置 (json)

```json
{
  "component": true,
  "usingComponents": {},
  "properties": {
    "title": {
      "type": String,
      "value": ""
    },
    "type": {
      type: Number,
      value: 1
    }
  }
}
```

### 3. 组件逻辑 (js)

```javascript
Component({
  properties: {
    title: {
      type: String,
      value: ''
    }
  },

  data: {
    internalValue: ''
  },

  methods: {
    onTap() {
      this.triggerEvent('customevent', { value: this.data.internalValue })
    }
  }
})
```

## 组件通信

### 父组件 → 子组件（属性绑定）

```xml
<!-- 父组件 wxml -->
<my-component title="标题" />
```

### 子组件 → 父组件（事件触发）

```javascript
// 子组件
this.triggerEvent('myevent', { detail: { value: 123 } })

// 父组件 wxml
<my-component bind:myevent="onMyEvent" />

// 父组件 js
onMyEvent(e) {
  console.log(e.detail.value) // 123
}
```

## 插槽使用

### 单插槽

```xml
<!-- 子组件 wxml -->
<view class="container">
  <slot></slot>
</view>

<!-- 父组件 -->
<my-component>
  <view>插入的内容</view>
</my-component>
```

### 多插槽

```json
{
  "component": true,
  "options": {
    "multipleSlots": true
  }
}
```

```xml
<!-- 子组件 -->
<slot name="header"></slot>
<slot name="body"></slot>
<slot name="footer"></slot>

<!-- 父组件 -->
<my-component>
  <view slot="header">头部</view>
  <view slot="body">内容</view>
  <view slot="footer">底部</view>
</my-component>
```

## 注意事项

- 组件需要在自己的 `json` 中声明 `component: true`
- 组件的 `data` 和 `properties` 区别：`data` 是内部数据，`properties` 是外部传入的属性
- 组件的方法放在 `methods` 对象中
- 组件的生命周期：created → attached → ready → detached
- 使用 `relations` 实现组件间关系（如 list 和 list-item）

## 适用场景

- 多个页面重复使用的 UI 模块
- 复杂的表单控件
- 可复用的业务组件（如评价星级、标签选择等）
