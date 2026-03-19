// 数维数据管家系统 - 表单逻辑 (统一版本)
// 版本: 2.0 - 2024-03-14
console.log('=== form.js 开始加载 ===');

// 全局变量
window.currentStep = 1;
window.totalSteps = 6;
console.log('全局变量初始化完成: currentStep=' + window.currentStep + ', totalSteps=' + window.totalSteps);

// ==================== 初始化 ====================
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== DOMContentLoaded 事件触发 ===');
    console.log('开始初始化表单...');
    initForm();
});

function initForm() {
    console.log('initForm() 开始执行');
    
    // 初始化显示
    updateStepDisplay();
    
    // 绑定按钮事件
    var nextBtn = document.getElementById('nextBtn');
    var prevBtn = document.getElementById('prevBtn');
    var submitBtn = document.getElementById('submitBtn');
    
    console.log('按钮元素:', {
        nextBtn: nextBtn ? '找到' : '未找到',
        prevBtn: prevBtn ? '找到' : '未找到',
        submitBtn: submitBtn ? '找到' : '未找到'
    });
    
    if (nextBtn) {
        nextBtn.addEventListener('click', handleNextStep);
        console.log('nextBtn 事件绑定成功');
    }
    if (prevBtn) {
        prevBtn.addEventListener('click', handlePrevStep);
        console.log('prevBtn 事件绑定成功');
    }
    if (submitBtn) {
        submitBtn.addEventListener('click', handleSubmit);
        console.log('submitBtn 事件绑定成功');
    }
    
    // 绑定表单提交事件
    var form = document.getElementById('surveyForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            handleSubmit();
        });
        console.log('form 事件绑定成功');
    }
    
    // 初始化省份选择
    initProvinceSelect();
    
    // 初始化"其他"选项
    initOtherOptions();
    
    console.log('initForm() 执行完成');
}

// ==================== 步骤切换 ====================
function handleNextStep() {
    console.log('=== handleNextStep 被调用 ===');
    console.log('当前步骤:', window.currentStep);
    console.log('总步骤:', window.totalSteps);
    
    // 验证当前步骤
    console.log('开始验证当前步骤...');
    var errors = validateCurrentStep();
    console.log('验证结果 - 错误数量:', errors.length);
    console.log('错误列表:', errors);
    
    if (errors.length > 0) {
        console.log('有错误，显示错误提示');
        showValidationErrors(errors);
        return;
    }
    
    // 切换到下一步
    if (window.currentStep < window.totalSteps) {
        console.log('切换到下一步:', window.currentStep + 1);
        goToStep(window.currentStep + 1);
    } else {
        console.log('已经是最后一步');
    }
}

function handlePrevStep() {
    console.log('handlePrevStep called, currentStep:', window.currentStep);
    
    if (window.currentStep > 1) {
        goToStep(window.currentStep - 1);
    }
}

function goToStep(step) {
    console.log('goToStep:', step);
    
    // 隐藏当前步骤
    var currentSection = document.querySelector('.form-section[data-section="' + window.currentStep + '"]');
    if (currentSection) {
        currentSection.classList.remove('active');
    }
    
    // 更新步骤
    window.currentStep = step;
    
    // 显示新步骤
    var newSection = document.querySelector('.form-section[data-section="' + window.currentStep + '"]');
    if (newSection) {
        newSection.classList.add('active');
    }
    
    // 更新显示
    updateStepDisplay();
    
    // 滚动到顶部
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==================== 显示更新 ====================
function updateStepDisplay() {
    updateProgressBar();
    updateStepIndicator();
    updateButtons();
}

function updateProgressBar() {
    var progress = (window.currentStep / window.totalSteps) * 100;
    
    var progressBar = document.getElementById('progress-bar');
    var progressText = document.getElementById('progress-text');
    
    if (progressBar) {
        progressBar.style.width = progress + '%';
    }
    if (progressText) {
        progressText.textContent = Math.round(progress) + '%';
    }
    
    // 更新进度线
    var progressLine = document.getElementById('progress-line');
    if (progressLine) {
        progressLine.style.width = ((window.currentStep - 1) / (window.totalSteps - 1) * 100) + '%';
    }
    
    // 更新进度节点
    var segments = document.querySelectorAll('#progress-segments .progress-node-glass');
    segments.forEach(function(seg, index) {
        seg.classList.remove('completed', 'active');
        if (index < window.currentStep - 1) {
            seg.classList.add('completed');
        } else if (index === window.currentStep - 1) {
            seg.classList.add('active');
        }
    });
}

function updateStepIndicator() {
    var steps = document.querySelectorAll('.step-glass');
    steps.forEach(function(step, index) {
        var stepNum = index + 1;
        step.classList.remove('active', 'completed');
        
        var circle = step.querySelector('.step-circle-glass');
        
        if (stepNum < window.currentStep) {
            step.classList.add('completed');
            if (circle) {
                circle.innerHTML = '<i class="bi bi-check"></i>';
            }
        } else if (stepNum === window.currentStep) {
            step.classList.add('active');
            if (circle) {
                circle.textContent = stepNum;
            }
        } else {
            if (circle) {
                circle.textContent = stepNum;
            }
        }
    });
}

function updateButtons() {
    var prevBtn = document.getElementById('prevBtn');
    var nextBtn = document.getElementById('nextBtn');
    var submitBtn = document.getElementById('submitBtn');
    
    if (prevBtn) {
        prevBtn.style.display = window.currentStep === 1 ? 'none' : 'block';
    }
    if (nextBtn) {
        nextBtn.style.display = window.currentStep === window.totalSteps ? 'none' : 'block';
    }
    if (submitBtn) {
        submitBtn.style.display = window.currentStep === window.totalSteps ? 'block' : 'none';
    }
}

// ==================== 表单验证 ====================
function validateCurrentStep() {
    var errors = [];
    var currentSection = document.querySelector('.form-section[data-section="' + window.currentStep + '"]');
    
    if (!currentSection) {
        console.error('Current section not found for step:', window.currentStep);
        return errors;
    }
    
    var requiredInputs = currentSection.querySelectorAll('[required]');
    var checkedRadioGroups = {};
    
    requiredInputs.forEach(function(input) {
        // 跳过禁用的输入框
        if (input.disabled) return;
        
        // 获取问题标签
        var questionDiv = input.closest('.form-question-glass');
        var labelEl = questionDiv ? questionDiv.querySelector('.question-label-glass') : null;
        var labelText = labelEl ? labelEl.textContent.replace('*', '').trim() : input.name;
        
        if (input.type === 'radio') {
            // 单选按钮组验证
            var groupName = input.name;
            if (!checkedRadioGroups[groupName]) {
                checkedRadioGroups[groupName] = true;
                var checked = currentSection.querySelector('input[name="' + groupName + '"]:checked');
                if (!checked) {
                    errors.push(labelText);
                    highlightError(questionDiv);
                } else {
                    clearError(questionDiv);
                }
            }
        } else if (input.type === 'checkbox') {
            // 复选框组验证 - 检查是否至少有一个被选中
            var groupName = input.name;
            var anyChecked = currentSection.querySelector('input[name="' + groupName + '"]:checked');
            if (!anyChecked && !errors.some(function(e) { return e.includes(labelText); })) {
                // 只在第一个checkbox时添加错误
                var firstCheckbox = currentSection.querySelector('input[name="' + groupName + '"]');
                if (input === firstCheckbox) {
                    errors.push(labelText);
                    highlightError(questionDiv);
                }
            } else if (anyChecked) {
                clearError(questionDiv);
            }
        } else {
            // 文本输入框验证
            if (!input.value || !input.value.trim()) {
                errors.push(labelText);
                input.style.borderColor = '#FF6B6B';
                input.style.background = 'rgba(255, 107, 107, 0.05)';
            } else {
                input.style.borderColor = '';
                input.style.background = '';
            }
        }
    });
    
    return errors;
}

function highlightError(element) {
    if (element) {
        element.style.borderLeftColor = '#FF6B6B';
        element.style.background = 'rgba(255, 107, 107, 0.05)';
    }
}

function clearError(element) {
    if (element) {
        element.style.borderLeftColor = '';
        element.style.background = '';
    }
}

function showValidationErrors(errors) {
    // 移除已存在的提示
    var existingAlert = document.getElementById('validation-alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    // 创建提示框
    var alertDiv = document.createElement('div');
    alertDiv.id = 'validation-alert';
    alertDiv.style.cssText = 'position: fixed; top: 20px; right: 20px; background: linear-gradient(135deg, #FF6B6B 0%, #ee5a5a 100%); color: white; padding: 16px 24px; border-radius: 12px; box-shadow: 0 4px 20px rgba(255, 107, 107, 0.4); z-index: 10000; max-width: 400px;';
    
    var errorList = errors.map(function(e) { return '<li>' + e + '</li>'; }).join('');
    
    alertDiv.innerHTML = '<div style="display: flex; align-items: flex-start; gap: 12px;">' +
        '<i class="bi bi-exclamation-triangle-fill" style="font-size: 20px; margin-top: 2px;"></i>' +
        '<div>' +
        '<div style="font-weight: 600; margin-bottom: 8px;">请完成以下必填项：</div>' +
        '<ul style="margin: 0; padding-left: 20px; font-size: 14px;">' + errorList + '</ul>' +
        '</div>' +
        '<button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: white; font-size: 20px; cursor: pointer; padding: 0; margin-left: auto;">&times;</button>' +
        '</div>';
    
    document.body.appendChild(alertDiv);
    
    // 5秒后自动移除
    setTimeout(function() {
        if (alertDiv.parentElement) {
            alertDiv.style.opacity = '0';
            alertDiv.style.transition = 'opacity 0.3s ease';
            setTimeout(function() {
                if (alertDiv.parentElement) {
                    alertDiv.remove();
                }
            }, 300);
        }
    }, 5000);
}

// ==================== 评估次数检查 ====================
function checkEvalLimit(token, callback) {
    fetch('/api/v1/evaluation/vip-status', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
    .then(function(response) {
        if (response.status === 401) {
            callback(false, '登录已过期，请重新登录');
            return;
        }
        return response.json();
    })
    .then(function(data) {
        if (data) {
            callback(data.can_evaluate, data.message);
        }
    })
    .catch(function(error) {
        console.error('检查评估次数失败:', error);
        callback(true); // 出错时允许继续
    });
}

// ==================== 表单提交 ====================
function handleSubmit() {
    console.log('handleSubmit called');
    
    // 验证最后一步
    var errors = validateCurrentStep();
    if (errors.length > 0) {
        showValidationErrors(errors);
        return;
    }
    
    // 检查登录状态
    var token = localStorage.getItem('token');
    if (!token) {
        alert('请先登录后再提交评估');
        window.location.href = '/login';
        return;
    }
    
    // 先检查评估次数
    checkEvalLimit(token, function(canEvaluate, message) {
        if (!canEvaluate) {
            alert(message || '评估次数已用完，VIP用户无限制');
            return;
        }
        
        // 显示加载动画
        var loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.classList.add('active');
        }
        
        // 收集表单数据
        var formData = collectFormData();
        console.log('Form data:', formData);
        
        // 提交到后端
        fetch('/api/v1/evaluation/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ form_data: formData })
        })
        .then(function(response) {
            if (response.status === 401) {
                alert('登录已过期，请重新登录');
                localStorage.removeItem('token');
                localStorage.removeItem('userInfo');
                window.location.href = '/login';
                return null;
            }
            if (response.status === 403) {
                return response.json().then(function(data) {
                    alert(data.detail && data.detail.message || '评估次数已用完，请联系管理员');
                    if (loadingOverlay) {
                        loadingOverlay.classList.remove('active');
                    }
                    return null;
                });
            }
            if (!response.ok) {
                return response.json().then(function(data) {
                    throw new Error(data.detail || 'API请求失败: ' + response.status);
                });
            }
            return response.json();
        })
        .then(function(result) {
            if (result) {
                console.log('Evaluation result:', result);
                localStorage.removeItem('viewReportId');
                localStorage.setItem('reportData', JSON.stringify(result));
                window.location.href = '/report';
            }
        })
        .catch(function(error) {
            console.error('Submit error:', error);
            if (loadingOverlay) {
                loadingOverlay.classList.remove('active');
            }
            alert('提交失败，请稍后重试: ' + error.message);
        });
    });
}

function collectFormData() {
    var formData = {};
    var form = document.getElementById('surveyForm');
    var elements = form.elements;
    
    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        if (!element.name) continue;
        
        if (element.type === 'radio') {
            if (element.checked) {
                formData[element.name] = element.value;
            }
        } else if (element.type === 'checkbox') {
            if (element.checked) {
                if (!formData[element.name]) {
                    formData[element.name] = [];
                }
                formData[element.name].push(element.value);
            }
        } else if (element.name === 'province' || element.name === 'city') {
            // 跳过省份和城市，后面单独处理
            continue;
        } else {
            formData[element.name] = element.value;
        }
    }
    
    // 处理省份和城市
    var province = document.getElementById('province');
    var city = document.getElementById('city');
    if (province && city && province.value && city.value) {
        formData['location'] = province.value + ' - ' + city.value;
    }
    
    // 处理"其他"选项
    processOtherOptions(formData);
    
    return formData;
}

function processOtherOptions(formData) {
    var otherFields = [
        { field: 'data_source', input: 'data_source_other' },
        { field: 'security_cert', input: 'security_cert_other' },
        { field: 'data_type', input: 'data_type_other' },
        { field: 'data_product', input: 'data_product_other' },
        { field: 'data_format', input: 'data_format_other' }
    ];
    
    otherFields.forEach(function(item) {
        if (formData[item.field] && Array.isArray(formData[item.field])) {
            var otherIndex = formData[item.field].indexOf('其他');
            if (otherIndex !== -1) {
                var otherInput = document.querySelector('input[name="' + item.input + '"]');
                if (otherInput && otherInput.value.trim()) {
                    formData[item.field][otherIndex] = '其他: ' + otherInput.value.trim();
                }
            }
        }
    });
    
    // 处理机构类型的"其他"
    if (formData['org_type'] === '其他') {
        var orgTypeOther = document.querySelector('input[name="org_type_other"]');
        if (orgTypeOther && orgTypeOther.value.trim()) {
            formData['org_type'] = '其他: ' + orgTypeOther.value.trim();
        }
    }
}

// ==================== 省份城市联动 ====================
var provinceCityData = {
    '北京市': ['东城区', '西城区', '朝阳区', '丰台区', '石景山区', '海淀区', '门头沟区', '房山区', '通州区', '顺义区', '昌平区', '大兴区', '怀柔区', '平谷区', '密云区', '延庆区'],
    '天津市': ['和平区', '河东区', '河西区', '南开区', '河北区', '红桥区', '东丽区', '西青区', '津南区', '北辰区', '武清区', '宝坻区', '滨海新区', '宁河区', '静海区', '蓟州区'],
    '河北省': ['石家庄市', '唐山市', '秦皇岛市', '邯郸市', '邢台市', '保定市', '张家口市', '承德市', '沧州市', '廊坊市', '衡水市'],
    '山西省': ['太原市', '大同市', '阳泉市', '长治市', '晋城市', '朔州市', '晋中市', '运城市', '忻州市', '临汾市', '吕梁市'],
    '内蒙古自治区': ['呼和浩特市', '包头市', '乌海市', '赤峰市', '通辽市', '鄂尔多斯市', '呼伦贝尔市', '巴彦淖尔市', '乌兰察布市', '兴安盟', '锡林郭勒盟', '阿拉善盟'],
    '辽宁省': ['沈阳市', '大连市', '鞍山市', '抚顺市', '本溪市', '丹东市', '锦州市', '营口市', '阜新市', '辽阳市', '盘锦市', '铁岭市', '朝阳市', '葫芦岛市'],
    '吉林省': ['长春市', '吉林市', '四平市', '辽源市', '通化市', '白山市', '松原市', '白城市', '延边州'],
    '黑龙江省': ['哈尔滨市', '齐齐哈尔市', '鸡西市', '鹤岗市', '双鸭山市', '大庆市', '伊春市', '佳木斯市', '七台河市', '牡丹江市', '黑河市', '绥化市', '大兴安岭地区'],
    '上海市': ['黄浦区', '徐汇区', '长宁区', '静安区', '普陀区', '虹口区', '杨浦区', '闵行区', '宝山区', '嘉定区', '浦东新区', '金山区', '松江区', '青浦区', '奉贤区', '崇明区'],
    '江苏省': ['南京市', '无锡市', '徐州市', '常州市', '苏州市', '南通市', '连云港市', '淮安市', '盐城市', '扬州市', '镇江市', '泰州市', '宿迁市'],
    '浙江省': ['杭州市', '宁波市', '温州市', '嘉兴市', '湖州市', '绍兴市', '金华市', '衢州市', '舟山市', '台州市', '丽水市'],
    '安徽省': ['合肥市', '芜湖市', '蚌埠市', '淮南市', '马鞍山市', '淮北市', '铜陵市', '安庆市', '黄山市', '滁州市', '阜阳市', '宿州市', '六安市', '亳州市', '池州市', '宣城市'],
    '福建省': ['福州市', '厦门市', '莆田市', '三明市', '泉州市', '漳州市', '南平市', '龙岩市', '宁德市'],
    '江西省': ['南昌市', '景德镇市', '萍乡市', '九江市', '新余市', '鹰潭市', '赣州市', '吉安市', '宜春市', '抚州市', '上饶市'],
    '山东省': ['济南市', '青岛市', '淄博市', '枣庄市', '东营市', '烟台市', '潍坊市', '济宁市', '泰安市', '威海市', '日照市', '临沂市', '德州市', '聊城市', '滨州市', '菏泽市'],
    '河南省': ['郑州市', '开封市', '洛阳市', '平顶山市', '安阳市', '鹤壁市', '新乡市', '焦作市', '濮阳市', '许昌市', '漯河市', '三门峡市', '南阳市', '商丘市', '信阳市', '周口市', '驻马店市'],
    '湖北省': ['武汉市', '黄石市', '十堰市', '宜昌市', '襄阳市', '鄂州市', '荆门市', '孝感市', '荆州市', '黄冈市', '咸宁市', '随州市', '恩施州', '仙桃市', '潜江市', '天门市', '神农架林区'],
    '湖南省': ['长沙市', '株洲市', '湘潭市', '衡阳市', '邵阳市', '岳阳市', '常德市', '张家界市', '益阳市', '郴州市', '永州市', '怀化市', '娄底市', '湘西州'],
    '广东省': ['广州市', '韶关市', '深圳市', '珠海市', '汕头市', '佛山市', '江门市', '湛江市', '茂名市', '肇庆市', '惠州市', '梅州市', '汕尾市', '河源市', '阳江市', '清远市', '东莞市', '中山市', '潮州市', '揭阳市', '云浮市'],
    '广西壮族自治区': ['南宁市', '柳州市', '桂林市', '梧州市', '北海市', '防城港市', '钦州市', '贵港市', '玉林市', '百色市', '贺州市', '河池市', '来宾市', '崇左市'],
    '海南省': ['海口市', '三亚市', '三沙市', '儋州市', '五指山市', '琼海市', '文昌市', '万宁市', '东方市'],
    '重庆市': ['渝中区', '江北区', '南岸区', '九龙坡区', '沙坪坝区', '渝北区', '北碚区', '巴南区', '涪陵区', '万州区', '黔江区', '长寿区', '江津区', '合川区', '永川区', '南川区', '璧山区', '铜梁区', '潼南区', '荣昌区', '开州区', '梁平区', '武隆区', '城口县', '丰都县', '垫江县', '忠县', '云阳县', '奉节县', '巫山县', '巫溪县', '石柱县', '秀山县', '酉阳县', '彭水县'],
    '四川省': ['成都市', '自贡市', '攀枝花市', '泸州市', '德阳市', '绵阳市', '广元市', '遂宁市', '内江市', '乐山市', '南充市', '眉山市', '宜宾市', '广安市', '达州市', '雅安市', '巴中市', '资阳市', '阿坝州', '甘孜州', '凉山州'],
    '贵州省': ['贵阳市', '六盘水市', '遵义市', '安顺市', '毕节市', '铜仁市', '黔西南州', '黔东南州', '黔南州'],
    '云南省': ['昆明市', '曲靖市', '玉溪市', '保山市', '昭通市', '丽江市', '普洱市', '临沧市', '楚雄州', '红河州', '文山州', '西双版纳州', '大理州', '德宏州', '怒江州', '迪庆州'],
    '西藏自治区': ['拉萨市', '日喀则市', '昌都市', '林芝市', '山南市', '那曲市', '阿里地区'],
    '陕西省': ['西安市', '铜川市', '宝鸡市', '咸阳市', '渭南市', '延安市', '汉中市', '榆林市', '安康市', '商洛市'],
    '甘肃省': ['兰州市', '嘉峪关市', '金昌市', '白银市', '天水市', '武威市', '张掖市', '平凉市', '酒泉市', '庆阳市', '定西市', '陇南市', '临夏州', '甘南州'],
    '青海省': ['西宁市', '海东市', '海北州', '黄南州', '海南州', '果洛州', '玉树州', '海西州'],
    '宁夏回族自治区': ['银川市', '石嘴山市', '吴忠市', '固原市', '中卫市'],
    '新疆维吾尔自治区': ['乌鲁木齐市', '克拉玛依市', '吐鲁番市', '哈密市', '昌吉州', '博尔塔拉州', '巴音郭楞州', '阿克苏地区', '克孜勒苏州', '喀什地区', '和田地区', '伊犁州', '塔城地区', '阿勒泰地区']
};

function initProvinceSelect() {
    var provinceSelect = document.getElementById('province');
    if (provinceSelect) {
        provinceSelect.addEventListener('change', updateCities);
    }
}

function updateCities() {
    var provinceSelect = document.getElementById('province');
    var citySelect = document.getElementById('city');
    
    if (!provinceSelect || !citySelect) return;
    
    var selectedProvince = provinceSelect.value;
    
    // 清空城市选项
    citySelect.innerHTML = '<option value="">请选择城市</option>';
    
    if (selectedProvince && provinceCityData[selectedProvince]) {
        citySelect.disabled = false;
        provinceCityData[selectedProvince].forEach(function(city) {
            var option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });
    } else {
        citySelect.disabled = true;
        citySelect.innerHTML = '<option value="">请先选择省份</option>';
    }
}

// ==================== "其他"选项处理 ====================
function initOtherOptions() {
    // 处理所有"其他"选项
    document.querySelectorAll('input[value="其他"]').forEach(function(input) {
        input.addEventListener('change', handleOtherOptionChange);
    });
    
    // 处理同组单选按钮
    document.querySelectorAll('input[type="radio"]').forEach(function(radio) {
        var group = document.querySelectorAll('input[name="' + radio.name + '"]');
        var hasOther = Array.from(group).some(function(r) { return r.value === '其他'; });
        
        if (hasOther) {
            radio.addEventListener('change', handleOtherOptionChange);
        }
    });
}

function handleOtherOptionChange(e) {
    var input = e.target;
    var parentDiv = input.closest('.form-question-glass');
    if (!parentDiv) return;
    
    var wrapper = parentDiv.querySelector('.other-input-wrapper-glass');
    if (!wrapper) return;
    
    var innerInput = wrapper.querySelector('input, textarea');
    
    if (input.type === 'checkbox') {
        // 复选框：勾选显示，取消隐藏
        if (input.checked) {
            wrapper.classList.remove('d-none');
            if (innerInput) {
                innerInput.disabled = false;
                setTimeout(function() { innerInput.focus(); }, 100);
            }
        } else {
            wrapper.classList.add('d-none');
            if (innerInput) {
                innerInput.disabled = true;
                innerInput.value = '';
            }
        }
    } else if (input.type === 'radio') {
        // 单选按钮：检查是否选中"其他"
        var isSelected = input.checked && input.value === '其他';
        
        if (isSelected) {
            wrapper.classList.remove('d-none');
            if (innerInput) {
                innerInput.disabled = false;
                setTimeout(function() { innerInput.focus(); }, 100);
            }
        } else if (input.checked) {
            // 选中了其他选项，隐藏"其他"输入框
            wrapper.classList.add('d-none');
            if (innerInput) {
                innerInput.disabled = true;
                innerInput.value = '';
            }
        }
    }
}

// ==================== 其他功能 ====================
function toggleDeptInput() {
    var radios = document.getElementsByName('has_data_dept');
    var deptInput = document.getElementById('dept_name');
    
    if (!deptInput) return;
    
    var selectedValue = null;
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            selectedValue = radios[i].value;
            break;
        }
    }
    
    if (selectedValue === '是') {
        deptInput.disabled = false;
        deptInput.placeholder = '请填写部门名称';
        deptInput.focus();
    } else if (selectedValue === '否') {
        deptInput.disabled = true;
        deptInput.value = '';
        deptInput.placeholder = '已选择"否"，无需填写';
    }
}

function toggleCloudProviderInput() {
    var radios = document.getElementsByName('storage_location');
    var cloudProviderInput = document.getElementById('cloud_provider');
    
    if (!cloudProviderInput) return;
    
    var selectedValue = null;
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            selectedValue = radios[i].value;
            break;
        }
    }
    
    if (selectedValue === '自有服务器') {
        cloudProviderInput.disabled = true;
        cloudProviderInput.value = '';
    } else if (selectedValue === '云存储' || selectedValue === '混合存储') {
        cloudProviderInput.disabled = false;
        cloudProviderInput.focus();
    }
}

// 全局暴露必要函数
window.toggleOtherInput = handleOtherOptionChange;
window.updateCities = updateCities;
window.toggleDeptInput = toggleDeptInput;
window.toggleCloudProviderInput = toggleCloudProviderInput;
