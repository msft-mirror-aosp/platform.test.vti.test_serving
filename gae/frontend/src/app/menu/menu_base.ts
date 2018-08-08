export abstract class MenuBaseClass {
  count = -1;

  pageSizeOptions = [20, 50, 100, 200];
  pageSize = 100;
  pageIndex = 0;

  protected constructor() {
  }
}
