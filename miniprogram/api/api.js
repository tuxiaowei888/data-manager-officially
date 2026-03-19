/**
 * 数维数据管家小程序 - API封装
 */

const app = getApp();

const request = (options) => {
  return new Promise((resolve, reject) => {
    const token = app.getToken();
    
    wx.request({
      url: `${app.globalData.baseUrl}${options.url}`,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data);
        } else if (res.statusCode === 401) {
          app.clearUserInfo();
          wx.redirectTo({ url: '/pages/index/index' });
          reject({ message: '未授权，请重新登录' });
        } else {
          reject(res.data || { message: '请求失败' });
        }
      },
      fail: (err) => {
        reject({ message: '网络请求失败' });
      }
    });
  });
};

const authApi = {
  login: (username, password) => {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${app.globalData.baseUrl}/auth/login`,
        method: 'POST',
        header: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(res.data || { message: '登录失败' });
          }
        },
        fail: () => reject({ message: '网络请求失败' })
      });
    });
  },
  
  register: (data) => {
    return request({
      url: '/auth/register',
      method: 'POST',
      data
    });
  },
  
  getUserInfo: () => {
    return request({
      url: '/auth/me',
      method: 'GET'
    });
  }
};

const evaluationApi = {
  evaluate: (formData) => {
    return request({
      url: '/evaluation/evaluate',
      method: 'POST',
      data: { form_data: formData }
    });
  },
  
  getHistory: (userId, limit = 10) => {
    return request({
      url: `/evaluation/user/${userId}/history?limit=${limit}`,
      method: 'GET'
    });
  },
  
  getResult: (resultId) => {
    return request({
      url: `/evaluation/${resultId}`,
      method: 'GET'
    });
  },
  
  getVipStatus: () => {
    return request({
      url: '/evaluation/vip-status',
      method: 'GET'
    });
  }
};

const reportApi = {
  getList: (limit = 20, offset = 0) => {
    return request({
      url: `/reports?limit=${limit}&offset=${offset}`,
      method: 'GET'
    });
  },
  
  getDetail: (reportId) => {
    return request({
      url: `/reports/${reportId}`,
      method: 'GET'
    });
  }
};

module.exports = {
  authApi,
  evaluationApi,
  reportApi
};
