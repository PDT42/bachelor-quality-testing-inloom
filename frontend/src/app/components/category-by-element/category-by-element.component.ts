import { Component, Input, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Evaluation } from 'src/app/classes/evaluation';
import { EvaluationService } from 'src/app/services/evaluation.service';
import { MetaEvalService } from 'src/app/services/metaeval.service';

@Component({
  selector: 'app-category-by-element',
  templateUrl: './category-by-element.component.html',
  styleUrls: ['./category-by-element.component.css'],
})
export class CategoryByElementComponent implements OnInit {
  @Input()
  manEvalId: string;
  @Input()
  autoEvalId: string;

  constructor(
    public evaluationService: EvaluationService,
    public metaEvalService: MetaEvalService
    ) {}

  ngOnInit(): void {}

  getExpertTypeCategoryItems(): Observable<Object[]> {
    let resultCategoryLabels = {
      M: 'MISSING',
      E: 'ERROR',
      W: 'WARNING',
      C: 'CORRECT',
      I: 'INFO',
    };
    let resultCategoryColors = {
      M: '#d91414',
      E: '#de5047',
      W: '#ebda46',
      C: '#5fab46',
      I: '#3b87a1',
    };

    if (this.manEvalId && this.autoEvalId) {
      let resultCategoryItems$: Observable<Object[]> = new Observable((sub) => {
        // Create a map to hold the items
        let resultCategoryItems: Map<string, Object> = new Map();

        this.evaluationService
          .getEvaluation(this.autoEvalId)
          .subscribe((autoEval: Evaluation) => {
            // Collect all expert elements
            // and assigned categories
            autoEval.results.map((res) => {
              if (res) {
                let resultCategoryItem: Object = {
                  'auto-eval-category': res.result_category,
                  'auto-eval-category-color':
                    resultCategoryColors[res.result_category],
                  'auto-eval-category-label':
                    resultCategoryLabels[res.result_category],
                  'result-category-item': this.createResultKey(
                    res.expert_element
                  ),
                  'man-eval-category': 'M',
                  'man-eval-category-color': resultCategoryColors['M'],
                  'man-eval-category-label': resultCategoryLabels['M'],
                };

                // Add the created item to the map
                resultCategoryItems.set(
                  this.createResultKey(res.expert_element),
                  resultCategoryItem
                );
              }
            });

            this.evaluationService
              .getEvaluation(this.manEvalId)
              .subscribe((manEval: Evaluation) => {
                manEval.results.map((res) => {
                  if (res) {
                    let itemKey = this.createResultKey(res.expert_element);

                    let resultCategoryItem = resultCategoryItems.get(itemKey);

                    if (resultCategoryItem) {
                      resultCategoryItem['man-eval-category'] =
                        res.result_category;
                      resultCategoryItem['man-eval-category-color'] =
                        resultCategoryColors[res.result_category];
                      resultCategoryItem['man-eval-category-label'] =
                        resultCategoryLabels[res.result_category];

                      // Update the items map
                    } else {
                      resultCategoryItem = {
                        'man-eval-category': res.result_category,
                        'man-eval-category-color':
                          resultCategoryColors[res.result_category],
                        'man-eval-category-label':
                          resultCategoryLabels[res.result_category],
                        'result-category-item': this.createResultKey(
                          res.expert_element
                        ),
                        'auto-eval-category': 'M',
                        'auto-eval-category-color':
                          resultCategoryColors['M'],
                        'auto-eval-category-label':
                          resultCategoryLabels['M'],
                      };
                    }
                    resultCategoryItems.set(itemKey, resultCategoryItem);
                  }

                  sub.next(Array.from(resultCategoryItems.values()));
                });
              });
          });
      });
      return resultCategoryItems$;
    }
  }

  createResultKey(expertElement: Object): string {
    return (
      expertElement['element_type'] + ' - ' + expertElement['element_label']
    );
  }

  getCategoryColor(color: string): string {
    return '';
  }
}
