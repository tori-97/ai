<template>
    <!-- Graph -->
    <div class="content-container">
        <canvas id="graph"></canvas>
    </div>
</template>
<script lang="ts" setup>
    import { Chart, registerables } from 'chart.js'
    import annotation from 'chartjs-plugin-annotation'
    import { onMounted, defineExpose } from 'vue'
    import { PageInfoType } from '@/utils/types';

    Chart.register(...registerables, annotation)

    let ctx: HTMLCanvasElement
    let chart: Chart

    type AnnotationType = {
        [key: string]: object
        bot: {
            xValue: string
            yValue: number
            type: string
            backgroundColor: string
            backgroundShadowColor: string
        }
    }

    const createChart = () => {
        ctx = document.querySelector('#graph') as HTMLCanvasElement

        if (!ctx) return false

        const page_info = window.localStorage.getItem("page-info") as string 
        const pinfo = JSON.parse(page_info) as PageInfoType

        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: pinfo.training.times,
                datasets: [
                    {
                        label: pinfo.training.symbol,
                        data: pinfo.training.closes,
                    
                    },
                ],
                
            },
        
            options: {
                scales: {
                    x: {
                        ticks: {
                            stepSize: 50,
                            sampleSize: pinfo.training.times.length
                        }
                    }
                },
                plugins: {
                    annotation: {
                        annotations: {
                            bot: {
                                xValue: 1,
                                yValue: 2,
                                type: 'point',
                                backgroundColor: '#666',
                                backgroundShadowColor: '#222',
                            },
                        },
                    },
                },
            },
        })

        moveBot(0)
    }
    const moveBot = async (day: number) => {
        if (!chart) return false

        const annot = chart.config.options?.plugins?.annotation
            ?.annotations as AnnotationType

        if (!chart.config.data.labels) return false
        if (!annot) return false

        const bot = annot.bot

        if (!bot) return false

        bot.xValue = chart?.config?.data?.labels[day] as string
        bot.yValue = chart.config.data.datasets[0].data[day] as number

        setTimeout(() => {
            chart.update()
        }, 1000)
    }
    const updateChart = (
        symbol: string,
        labels: Array<string>,
        data: Array<number>,
    ) => {
        chart.clear()
        chart.config.data.labels = labels
        chart.config.data.datasets[0].label = symbol
        chart.config.data.datasets[0].data = data
        chart.update()
    }
    const resetBotPosition = () => {
        if (!chart.config.data.labels) return false

        const firtX = chart.config.data.labels[0]
        const firtY = chart.config.data.datasets[0].data[0]

        const annot = chart.config.options?.plugins?.annotation?.annotations as AnnotationType
        const bot = annot.bot

        bot.xValue = firtX as string
        bot.yValue = firtY as number

        chart.update()
    }

    onMounted(() => {
        createChart()
    })

    defineExpose({
        moveBot,
        updateChart,
        resetBotPosition,
    })
</script>
<style lang="scss" scoped>
    .content-container {
        width: 100%;
        height: 100%;

        overflow: hidden;
        overflow-y: auto;

        display: flex;
        flex-direction: column;
        align-items: center;

        padding: 0.8rem;
    }
</style>
