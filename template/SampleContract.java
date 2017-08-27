package com.etiantian.dywteacher.ui.{page};

import com.etiantian.dywteacher.entity.{Bean};
import com.etiantian.dywteacher.entity.Result;
import com.etiantian.dywteacher.mvpframe.base.BasePresenter;
import com.etiantian.dywteacher.mvpframe.base.IBaseModel;
import com.etiantian.dywteacher.mvpframe.base.IBaseView;

import rx.Observable;

/**
 * auto-generate
 * by zwx
 */
interface {alias}Contract {

    interface Model extends IBaseModel {
        Observable<Result<{Bean}>> {apiName}({TypedParams});
    }

    interface View extends IBaseView {
        void on{ApiName}Success({Bean} data);
    }

    abstract class Presenter extends BasePresenter<Model, View> {
        abstract void {apiName}({TypedParams});
    }
}
