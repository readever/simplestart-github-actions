/**
 * SimpleStart 前端配置文件
 * =======================================
 *
 * 这个文件用于配置前端与后端服务器的连接地址
 * 根据不同的部署环境，您需要修改 backendServer 的值
 *
 * 配置说明：
 * -----------
 * backendServer: 后端服务器地址
 *   - 留空字符串 "": 使用相对路径（推荐）
 *     适用于前后端部署在同一个域名下
 *     例如：当前页面 https://example.com/index.html
 *          API请求将发送到 https://example.com/api/xxx
 *
 *   - 完整URL: 指定具体的后端地址
 *     适用于前后端部署在不同域名或端口
 *     例如："http://localhost:8000" 或 "https://api.example.com"
 *
 * 部署场景示例：
 * ----------------
 * 1. 开发环境（前后端分离）：
 *    backendServer: "http://localhost:8000"
 *
 * 2. 生产环境（前后端同域）：
 *    backendServer: ""  // 留空即可
 *
 * 3. 生产环境（前后端分离）：
 *    backendServer: "https://api.yourdomain.com"
 *
 * 注意事项：
 * ---------
 * - 修改此文件后需要重新打包前端应用
 * - 在生产环境中，建议将敏感的后端地址隐藏在环境变量中
 * - 确保后端服务器已配置CORS，允许前端域名访问
 *
 * 启动后端示例：
 * --------------
 * ss app.py --port 8000 --allow-origins "*"
 * （--allow-origins 参数用于允许跨域访问）
 */

// 前端配置文件 - SimpleStart
// 修改这个文件来配置后端服务器地址
// 默认留空表示使用当前页面地址

window.SS_CONFIG = {
    backendServer: "" //"https://hz-t3.matpool.com:26076" //""
};