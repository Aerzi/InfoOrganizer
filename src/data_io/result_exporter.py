"""结果输出模块"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from ..utils.logger import logger


class ResultExporter:
    """结果导出器（支持Markdown/Excel/图表，动态适配自定义维度）"""
    
    def __init__(self, output_dir: str = "output"):
        """
        初始化结果导出器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f"初始化结果导出器，输出目录: {output_dir}")
    
    def export_markdown(self, results: Dict[str, Any], analysis_type: str = "双场景") -> str:
        """
        导出Markdown报告
        
        Args:
            results: 分析结果字典
            analysis_type: 分析类型（请求/反馈/双场景）
            
        Returns:
            Markdown文件路径
        """
        logger.info(f"生成Markdown报告: {analysis_type}")
        
        # 获取自定义维度
        dimensions = results.get("维度", [])
        dim_str = ",".join(dimensions) if dimensions else "通用"
        
        # 生成报告内容
        md_content = self._generate_markdown_content(results, analysis_type, dim_str)
        
        # 保存文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"PPT语料分析报告_{dim_str}_{timestamp}.md"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info(f"Markdown报告已保存: {filepath}")
        return str(filepath)
    
    def _generate_markdown_content(self, results: Dict[str, Any], 
                                   analysis_type: str, dim_str: str) -> str:
        """
        生成Markdown报告内容
        
        Args:
            results: 分析结果字典
            analysis_type: 分析类型
            dim_str: 维度字符串
            
        Returns:
            Markdown内容
        """
        dimensions = results.get("维度", [])
        
        # 报告标题
        md = f"# PPT主题生成场景语料分析报告（聚焦：{dim_str}）\n\n"
        md += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md += f"**分析类型**: {analysis_type}\n\n"
        md += "---\n\n"
        
        # 1. 核心分析结论
        md += "## 1. 核心分析结论\n\n"
        
        # 1.1 数据概览
        md += "### 1.1 数据概览\n\n"
        if "基础统计" in results:
            stats = results["基础统计"]
            md += f"- **总语料数**: {stats.get('总语料数', 0)}\n"
            md += f"- **{dim_str}相关语料数**: {stats.get('相关语料数', 0)}，占比：{stats.get('相关占比', '0%')}\n"
            
            if "类型分布" in stats:
                type_dist = stats["类型分布"]
                type_str = "、".join([f"{k}({v}条)" for k, v in type_dist.items()])
                md += f"- **语料类型分布**: {type_str}\n"
            
            md += "\n"
        
        # 1.2 请求语料分析
        if "请求分析" in results:
            md += f"### 1.2 {dim_str}-请求语料分析（需求分析）\n\n"
            request_results = results["请求分析"]
            
            # 需求分类
            if "需求分类" in request_results:
                demand_cat = request_results["需求分类"]
                top_demands = sorted(demand_cat.items(), key=lambda x: x[1], reverse=True)[:3]
                md += "- **核心需求**: " + "、".join([f"{k}({v}条)" for k, v in top_demands]) + "\n"
            
            # 关联特征
            if "关联特征" in request_results:
                associations = request_results["关联特征"]
                for dim, words in associations.items():
                    if words:
                        md += f"- **「{dim}」常关联**: {', '.join(words[:5])}\n"
            
            # 场景分布
            if "场景分布" in request_results:
                scenes = request_results["场景分布"]
                top_scenes = sorted(scenes.items(), key=lambda x: x[1], reverse=True)[:3]
                md += "- **主流场景**: " + "、".join([f"{k}({v}条)" for k, v in top_scenes]) + "\n"
            
            md += "\n"
        
        # 1.3 反馈语料分析
        if "反馈分析" in results:
            md += f"### 1.3 {dim_str}-反馈语料分析（效果反馈）\n\n"
            feedback_results = results["反馈分析"]
            
            # 情感分布
            if "情感分布" in feedback_results:
                sentiment = feedback_results["情感分布"]
                total = sum(sentiment.values())
                sentiment_str = "、".join([
                    f"{k}({v}条, {v/total*100:.1f}%)" 
                    for k, v in sentiment.items()
                ]) if total > 0 else "无数据"
                md += f"- **情感分布**: {sentiment_str}\n"
            
            # 问题分类
            if "问题分类" in feedback_results:
                problems = feedback_results["问题分类"]
                top_problems = sorted(problems.items(), key=lambda x: x[1], reverse=True)[:3]
                md += "- **核心问题**: " + "、".join([f"{k}({v}条)" for k, v in top_problems]) + "\n"
            
            # 优化建议
            if "优化建议" in feedback_results:
                suggestions = feedback_results["优化建议"]
                if suggestions:
                    md += "- **优化建议**:\n"
                    for i, suggestion in enumerate(suggestions[:3], 1):
                        md += f"  {i}. {suggestion}\n"
            
            md += "\n"
        
        # 2. 详细数据表格
        md += "## 2. 详细数据表格\n\n"
        
        # 2.1 词频统计表
        md += f"### 2.1 {dim_str}相关高频词统计\n\n"
        
        if "请求分析" in results and "维度相关词频Top10" in results["请求分析"]:
            md += "#### 请求语料高频词\n\n"
            md += "| 排名 | 关键词 | 频次 |\n"
            md += "|------|--------|------|\n"
            for i, (word, count) in enumerate(results["请求分析"]["维度相关词频Top10"], 1):
                md += f"| {i} | {word} | {count} |\n"
            md += "\n"
        
        if "反馈分析" in results and "维度相关词频Top10" in results["反馈分析"]:
            md += "#### 反馈语料高频词\n\n"
            md += "| 排名 | 关键词 | 频次 |\n"
            md += "|------|--------|------|\n"
            for i, (word, count) in enumerate(results["反馈分析"]["维度相关词频Top10"], 1):
                md += f"| {i} | {word} | {count} |\n"
            md += "\n"
        
        # 3. 可视化图表
        md += "## 3. 可视化图表\n\n"
        md += f"图表文件已保存在 `charts/` 目录下，包括：\n\n"
        md += f"- {dim_str}_请求_总体词频.png\n"
        md += f"- {dim_str}_请求_维度词频.png\n"
        md += f"- {dim_str}_请求_情感分布.png\n"
        md += f"- {dim_str}_反馈_总体词频.png\n"
        md += f"- {dim_str}_反馈_维度词频.png\n"
        md += f"- {dim_str}_反馈_情感分布.png\n"
        md += "\n"
        
        # 4. 分析说明
        md += "## 4. 分析说明\n\n"
        md += "本报告基于PPT主题生成场景的语料数据，采用本地化NLP分析方法，针对自定义维度进行多维度分析。\n\n"
        md += "**分析维度包括**：\n"
        md += "- 频次分布：统计自定义维度相关内容的出现频次和占比\n"
        md += "- 关联特征：分析自定义维度与其他诉求的关联关系\n"
        md += "- 情感倾向：识别用户对自定义维度的态度（正面/中性/负面）\n"
        md += "- 场景关联：分析自定义维度对应的PPT使用场景\n"
        md += "- 需求/问题分类：归类用户的具体需求和反馈问题\n"
        md += "\n"
        
        return md
    
    def export_excel(self, results: Dict[str, Any], analysis_type: str = "双场景") -> str:
        """
        导出Excel报告
        
        Args:
            results: 分析结果字典
            analysis_type: 分析类型
            
        Returns:
            Excel文件路径
        """
        logger.info(f"生成Excel报告: {analysis_type}")
        
        # 获取自定义维度
        dimensions = results.get("维度", [])
        dim_str = ",".join(dimensions) if dimensions else "通用"
        
        # 创建Excel writer
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"PPT语料分析报告_{dim_str}_{timestamp}.xlsx"
        filepath = self.output_dir / filename
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Sheet 1: 数据概览
            self._export_overview_sheet(results, writer)
            
            # Sheet 2: 请求分析
            if "请求分析" in results:
                self._export_request_sheet(results["请求分析"], writer)
            
            # Sheet 3: 反馈分析
            if "反馈分析" in results:
                self._export_feedback_sheet(results["反馈分析"], writer)
        
        logger.info(f"Excel报告已保存: {filepath}")
        return str(filepath)
    
    def _export_overview_sheet(self, results: Dict[str, Any], writer: pd.ExcelWriter) -> None:
        """导出概览Sheet"""
        data = []
        
        if "基础统计" in results:
            stats = results["基础统计"]
            for key, value in stats.items():
                if isinstance(value, dict):
                    for k, v in value.items():
                        data.append({"指标": f"{key}-{k}", "数值": v})
                else:
                    data.append({"指标": key, "数值": value})
        
        if data:
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name="数据概览", index=False)
    
    def _export_request_sheet(self, request_results: Dict[str, Any], writer: pd.ExcelWriter) -> None:
        """导出请求分析Sheet"""
        # 高频词
        if "维度相关词频Top10" in request_results:
            freq_data = [
                {"排名": i+1, "关键词": word, "频次": count}
                for i, (word, count) in enumerate(request_results["维度相关词频Top10"])
            ]
            df_freq = pd.DataFrame(freq_data)
            df_freq.to_excel(writer, sheet_name="请求-高频词", index=False)
        
        # 需求分类
        if "需求分类" in request_results:
            demand_data = [
                {"需求类别": k, "数量": v}
                for k, v in request_results["需求分类"].items()
            ]
            df_demand = pd.DataFrame(demand_data)
            df_demand.to_excel(writer, sheet_name="请求-需求分类", index=False)
    
    def _export_feedback_sheet(self, feedback_results: Dict[str, Any], writer: pd.ExcelWriter) -> None:
        """导出反馈分析Sheet"""
        # 高频词
        if "维度相关词频Top10" in feedback_results:
            freq_data = [
                {"排名": i+1, "关键词": word, "频次": count}
                for i, (word, count) in enumerate(feedback_results["维度相关词频Top10"])
            ]
            df_freq = pd.DataFrame(freq_data)
            df_freq.to_excel(writer, sheet_name="反馈-高频词", index=False)
        
        # 问题分类
        if "问题分类" in feedback_results:
            problem_data = [
                {"问题类别": k, "数量": v}
                for k, v in feedback_results["问题分类"].items()
            ]
            df_problem = pd.DataFrame(problem_data)
            df_problem.to_excel(writer, sheet_name="反馈-问题分类", index=False)
        
        # 优化建议
        if "优化建议" in feedback_results:
            suggestion_data = [
                {"序号": i+1, "建议内容": s}
                for i, s in enumerate(feedback_results["优化建议"])
            ]
            df_suggestion = pd.DataFrame(suggestion_data)
            df_suggestion.to_excel(writer, sheet_name="反馈-优化建议", index=False)
    
    def export_all(self, results: Dict[str, Any], analysis_type: str = "双场景") -> Dict[str, str]:
        """
        导出所有格式的报告
        
        Args:
            results: 分析结果字典
            analysis_type: 分析类型
            
        Returns:
            文件路径字典 {format: filepath}
        """
        logger.info("导出所有格式的报告")
        
        filepaths = {}
        
        # 导出Markdown
        try:
            md_path = self.export_markdown(results, analysis_type)
            filepaths["markdown"] = md_path
        except Exception as e:
            logger.error(f"导出Markdown失败: {str(e)}")
        
        # 导出Excel
        try:
            excel_path = self.export_excel(results, analysis_type)
            filepaths["excel"] = excel_path
        except Exception as e:
            logger.error(f"导出Excel失败: {str(e)}")
        
        logger.info(f"所有报告导出完成: {list(filepaths.keys())}")
        return filepaths

