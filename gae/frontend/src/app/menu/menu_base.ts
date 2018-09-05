/**
 * Copyright (C) 2018 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/** This class defines and/or implements the common properties and methods
 * used among menus.
 */
export abstract class MenuBaseClass {
  count = -1;

  loading = false;
  pageSizeOptions = [20, 50, 100, 200];
  pageSize = 100;
  pageIndex = 0;

  protected constructor() {
  }

  /** Returns an Observable which handles a response of count API.
   * @param additionalOperations A list of lambda functions.
   */
  getDefaultCountObservable(additionalOperations: any[] = []) {
    return {
      next: (response) => {
        this.count = response.count;
        for (const operation of additionalOperations) {
          operation(response);
        }
      },
      error: (error) => console.log(`[${error.status}] ${error.name}`)
    };
  }
}
