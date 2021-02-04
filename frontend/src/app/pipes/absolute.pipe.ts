import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'absolute'
})
export class AbsolutePipe implements PipeTransform {

  transform(num: number, ...args: any[]): any {
    return Math.abs(num);
  }

}
