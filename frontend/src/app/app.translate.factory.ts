import {TranslateHttpLoader} from '@ngx-translate/http-loader';
import {HttpClient} from '@angular/common/http';
import { environment } from '../environments/environment';

export function HttpLoaderFactory(http: HttpClient) {
  if(environment.production) {
    return new TranslateHttpLoader(http, './static/dist/assets/i18n/', '.json');
  } else {
    return new TranslateHttpLoader(http, './assets/i18n/', '.json');
  }
  
}