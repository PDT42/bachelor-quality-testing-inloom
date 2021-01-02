import { Component, Input, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { scaleLinear } from 'd3';
import { StatisticsService } from 'src/app/services/statistics.service';

@Component({
  selector: 'app-single-comparison',
  templateUrl: './single-comparison.component.html',
  styleUrls: ['./single-comparison.component.css'],
})
export class SingleComparisonComponent implements OnInit {
  @Input()
  testDataSetId: string;
  @Input()
  chartTitle: string;
  @Input()
  manEvalKey: string = null;
  @Input()
  autoEvalKey: string = null;

  tdsStatistics: Object;
  manEvalStats: Object;
  autoEvalStats: Object;

  constructor(public statisticsService: StatisticsService) {}

  ngOnInit(): void {
    this.statisticsService
      .getTDSStatistics(this.testDataSetId)
      .subscribe((result) => {
        // if the query has a body
        if (Object.keys(result).length > 0) {
          // story the tdsStatistics
          this.tdsStatistics = result;

          if (this.manEvalKey) {
            this.manEvalStats = result['man-eval-stats'][this.manEvalKey];
          } else {
            this.manEvalStats = result['avg-man-eval-stats'];
          }

          if (this.autoEvalKey) {
            this.autoEvalStats = result['auto-eval-stats'][this.autoEvalStats];
          } else {
            this.autoEvalStats = result['latest-auto-eval-stats'];
          }

          // Create chart
          this.createElementPerTypeChart();
        }
      });
  }

  createElementPerTypeChart(): void {
    const STATS_KEY = 'points-per-expert-element-type';
    const ROOT = d3.select('div#' + STATS_KEY);
    const ROOT_WIDTH = parseInt(ROOT.style('width'));
    const SVG_HEIGHT = 500;

    // Create svg root
    let svg_root = ROOT.append('svg')
      .attr('width', ROOT_WIDTH)
      .attr('height', SVG_HEIGHT);

    let _autoLocalStats: Map<string, number> = this.autoEvalStats[STATS_KEY];
    let _manLocalStats: Map<string, number> = this.manEvalStats[STATS_KEY];

    // Define x-scale
    let xItems = new Set([
      ...Object.keys(_manLocalStats),
      ...Object.keys(_autoLocalStats),
    ]);
    let xScale = d3
      .scaleBand()
      .range([0, ROOT_WIDTH])
      .padding(0.1)
      .domain(xItems);

    svg_root
      .append('g')
      .attr('transform', 'translate(25, 480)')
      .call(d3.axisBottom(xScale));

    // Define y-scale
    let yMax = d3.max(
      new Set<number>([
        ...Object.values(_manLocalStats),
        ...Object.values(_autoLocalStats),
      ])
    );
    let yScale = d3.scaleLinear().range([0, 480]).domain([0, yMax]);

    svg_root
      .append('g')
      .attr('transform', 'translate(25, 0)')
      .call(d3.axisLeft(yScale).ticks(0.5));

    svg_root
      .selectAll()
      .data(Object.entries(_manLocalStats))
      .enter()
      .append('rect')
      .attr('x', ([key]: [string, number]) => {
        console.log(key);
        return xScale(key);
      })
      .attr('y', ([, value]: [string, number]) => {
        console.log(value);
        return yScale(value);
      })
      .attr('height', ([, value]) => {
        return SVG_HEIGHT - yScale(value);
      })
      .attr('width', xScale.bandwidth());
  }
}
